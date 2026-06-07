import os
import logging
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Assuming the classifier is in src/guardrails/classifier.py
from ..guardrails.classifier import QueryClassifier

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """You are a facts-only mutual fund FAQ assistant for HDFC mutual fund schemes.
Your role is to answer factual questions using ONLY the provided context.

RULES:
1. Answer in a maximum of 3 sentences.
2. Use ONLY the information from the context below.
3. Include exactly ONE source citation link from the provided SOURCE URL.
4. Do NOT provide investment advice, opinions, or recommendations.
5. Do NOT compare fund performance or calculate returns.
6. If the context does not contain the answer, say:
   "I don't have this information in my sources."
7. End every response with: "Last updated from sources: {scrape_date}"

CONTEXT:
{retrieved_chunks}

SOURCE URL: {source_url}

USER QUESTION: {user_query}"""


class ResponseGenerator:
    def __init__(self, model_name="llama-3.1-8b-instant", temperature=0.1):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning(
                "GROQ_API_KEY is not set in environment variables. Generation will fail."
            )

        self.llm = ChatGroq(
            model=model_name,
            api_key=self.api_key,
            temperature=temperature,
            max_tokens=256,
        )

        self.prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=[
                "retrieved_chunks",
                "source_url",
                "user_query",
                "scrape_date",
            ],
        )

        self.chain = self.prompt | self.llm

        # Load advisory keywords for validation
        self.classifier = QueryClassifier()
        self.advisory_keywords = self.classifier.advisory_keywords

    def validate_response(self, answer: str) -> Dict[str, Any]:
        """
        Validates the generated response against business rules.
        """
        issues = []

        # Check sentence count (heuristic split by ". ")
        sentences = [s for s in answer.split(". ") if s.strip()]
        if (
            len(sentences) > 4
        ):  # Allowing 4 here just in case footer adds an extra sentence
            issues.append(f"Exceeds 3-sentence limit (found {len(sentences)})")

        # Check for advisory language
        answer_lower = answer.lower()
        for keyword in self.advisory_keywords:
            if keyword in answer_lower:
                issues.append(f"Contains advisory language: '{keyword}'")

        # Check for last-updated footer
        if "last updated from sources:" not in answer_lower:
            issues.append("Missing 'Last updated' footer")

        return {"valid": len(issues) == 0, "issues": issues}

    def generate(self, query: str, context_docs: list) -> str:
        """
        Generates an answer using the provided context documents.
        """
        if not context_docs:
            return "I don't have this information in my sources."

        # Extract context and metadata
        context_texts = []
        source_urls = set()
        scrape_dates = set()

        for doc in context_docs:
            context_texts.append(doc.page_content)
            if "source_url" in doc.metadata:
                source_urls.add(doc.metadata["source_url"])
            if "scrape_date" in doc.metadata:
                scrape_dates.add(doc.metadata["scrape_date"])

        retrieved_chunks = "\n\n---\n\n".join(context_texts)
        # We enforce exactly ONE source citation link from the provided SOURCE URL
        source_url = list(source_urls)[0] if source_urls else "Unknown Source"
        scrape_date = list(scrape_dates)[0] if scrape_dates else "Unknown Date"

        try:
            response = self.chain.invoke(
                {
                    "retrieved_chunks": retrieved_chunks,
                    "source_url": source_url,
                    "user_query": query,
                    "scrape_date": scrape_date,
                }
            )

            answer = response.content.strip()

            # Run validation (we can log issues or raise exceptions if strict enforcement is needed)
            validation = self.validate_response(answer)
            if not validation["valid"]:
                logger.warning(
                    f"Generated answer failed validation: {validation['issues']}"
                )
                # If it contains advisory language, we aggressively fallback
                if any(
                    "Contains advisory language" in issue
                    for issue in validation["issues"]
                ):
                    return "I cannot provide an answer as it may be construed as investment advice. Please consult a financial advisor."

            return answer

        except Exception as e:
            logger.error(f"Error during response generation: {e}")
            return "I encountered an error while generating the response. Please try again later."
