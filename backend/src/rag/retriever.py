import os
import logging
from typing import List, Tuple
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from ..ingestion.embedder import Embedder

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(
        self,
        db_dir: str = "./data/chroma",
        top_k: int = 5,
        similarity_threshold: float = 0.5,
    ):
        """
        Initializes the retriever with a local Chroma DB and HuggingFace BGE Embeddings.
        """
        self.db_dir = db_dir
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

        logger.info("Initializing Retriever and loading ChromaDB...")
        self.embedder = Embedder()

        if not os.path.exists(self.db_dir):
            raise FileNotFoundError(
                f"Chroma DB directory {self.db_dir} not found. Have you run the ingestion pipeline?"
            )

        self.vectorstore = Chroma(
            persist_directory=self.db_dir,
            embedding_function=self.embedder.get_embeddings(),
        )

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """
        Retrieves top_k chunks based on semantic similarity.
        Returns a list of (Document, score) tuples.
        Note: The score behavior depends on the distance metric used in Chroma (default is L2).
        For normalized embeddings, L2 distance is monotonically related to cosine similarity.
        """
        # Fetching top_k * 2 initially to allow reranker to work on a slightly broader set
        # Using similarity_search_with_relevance_scores if possible
        try:
            results = self.vectorstore.similarity_search_with_relevance_scores(
                query, k=self.top_k * 2
            )
        except Exception as e:
            logger.warning(
                f"Relevance scoring not supported directly, falling back to basic similarity: {e}"
            )
            # Fallback
            docs = self.vectorstore.similarity_search(query, k=self.top_k * 2)
            results = [(doc, 1.0) for doc in docs]

        # Filter by threshold (assuming relevance score is between 0 and 1 where 1 is perfect)
        # Langchain tries to normalize the L2 distance to a 0-1 similarity score.
        filtered_results = [
            (doc, score) for doc, score in results if score >= self.similarity_threshold
        ]

        # If filtering removed everything, return the top result regardless (soft fallback)
        if not filtered_results and results:
            filtered_results = results[:2]

        return filtered_results
