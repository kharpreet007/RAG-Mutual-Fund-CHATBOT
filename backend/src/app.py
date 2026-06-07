import os
import sys
import json
import logging
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --- Pydantic Models ---


class QueryRequest(BaseModel):
    query: str


class Citation(BaseModel):
    source_url: str
    scheme_name: str


class QueryResponse(BaseModel):
    status: str  # "success" | "refused" | "error"
    query: str
    answer: str
    citation: Optional[Citation] = None
    last_updated: Optional[str] = None
    educational_link: Optional[str] = None
    disclaimer: str = "Facts-only. No investment advice."


# --- Lazy-loaded global components ---
retriever = None
reranker = None
generator = None
classifier = None
refusal_handler = None


def init_components():
    """Initialize all heavy components once at startup."""
    global retriever, reranker, generator, classifier, refusal_handler

    from .rag.retriever import Retriever
    from .rag.reranker import ReRanker
    from .rag.generator import ResponseGenerator
    from .guardrails.classifier import QueryClassifier
    from .guardrails.refusal import RefusalHandler

    logger.info("Initializing RAG pipeline components...")
    retriever = Retriever(db_dir="data/chroma_db", top_k=5, similarity_threshold=0.3)
    reranker = ReRanker(top_k=3)
    generator = ResponseGenerator()
    classifier = QueryClassifier()
    refusal_handler = RefusalHandler()
    logger.info("All components initialized successfully.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup/shutdown."""
    init_components()
    yield
    logger.info("Shutting down...")


# --- FastAPI App ---

app = FastAPI(
    title="HDFC Mutual Fund FAQ Assistant",
    description="A facts-only FAQ assistant for 19 HDFC mutual fund schemes.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/schemes")
async def list_schemes():
    """List all available HDFC mutual fund schemes."""
    processed_dir = "data/processed"
    schemes = []

    if os.path.exists(processed_dir):
        for filename in sorted(os.listdir(processed_dir)):
            if filename.endswith(".json"):
                filepath = os.path.join(processed_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        schemes.append(
                            {
                                "scheme_name": data.get("scheme_name", ""),
                                "url": data.get("url", ""),
                                "nav": data.get("nav", ""),
                                "rating": data.get("rating", ""),
                                "expense_ratio": data.get("expense_ratio", ""),
                            }
                        )
                except Exception:
                    pass

    return {"schemes": schemes, "count": len(schemes)}


@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Main query endpoint.
    Flow: validate → PII check → classify → retrieve → re-rank → generate → validate → respond
    """
    query = request.query.strip()

    # Step 1: Validate input
    if not query:
        return QueryResponse(
            status="error", query=query, answer="Please enter a valid question."
        )

    # Step 2: Classify (PII check + advisory check)
    classification = classifier.classify_query(query)

    if classification == "PII_DETECTED":
        return QueryResponse(
            status="refused",
            query=query,
            answer=refusal_handler.get_refusal("PII_DETECTED"),
            educational_link="https://www.amfiindia.com/investor-corner/knowledge-center",
        )

    if classification == "ADVISORY":
        return QueryResponse(
            status="refused",
            query=query,
            answer=refusal_handler.get_refusal("ADVISORY"),
            educational_link="https://www.amfiindia.com/investor-corner/knowledge-center",
        )

    # Step 3: Retrieve relevant chunks
    try:
        raw_results = retriever.retrieve(query)
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        return QueryResponse(
            status="error",
            query=query,
            answer="An error occurred while searching for relevant information. Please try again.",
        )

    if not raw_results:
        return QueryResponse(
            status="success",
            query=query,
            answer="I don't have this information in my sources.",
        )

    # Step 4: Re-rank
    reranked = reranker.rerank(query, raw_results)

    if not reranked:
        return QueryResponse(
            status="success",
            query=query,
            answer="I don't have this information in my sources.",
        )

    # Extract top documents for generation
    top_docs = [doc for doc, score in reranked]

    # Step 5: Generate response
    try:
        answer = generator.generate(query, top_docs)
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return QueryResponse(
            status="error",
            query=query,
            answer="An error occurred while generating the response. Please try again.",
        )

    # Build citation from top result
    top_metadata = top_docs[0].metadata if top_docs else {}
    citation = Citation(
        source_url=top_metadata.get("source_url", ""),
        scheme_name=top_metadata.get("scheme_name", ""),
    )
    last_updated = top_metadata.get("scrape_date", None)

    return QueryResponse(
        status="success",
        query=query,
        answer=answer,
        citation=citation,
        last_updated=last_updated,
    )
