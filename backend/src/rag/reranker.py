import logging
from typing import List, Tuple
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class ReRanker:
    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def rerank(
        self, query: str, retrieved_docs: List[Tuple[Document, float]]
    ) -> List[Tuple[Document, float]]:
        """
        Heuristic-based re-ranking.
        Factors:
        - Cosine similarity score (base relevance): weight 0.5
        - Scheme name match in query: weight 0.3
        - Section relevance: weight 0.2
        """
        if not retrieved_docs:
            return []

        query_lower = query.lower()
        reranked = []

        for doc, base_score in retrieved_docs:
            metadata = doc.metadata
            scheme_name = metadata.get("scheme_name", "").lower()
            section = metadata.get("section", "").lower()

            # Base Score (0-1) weighted at 0.5
            final_score = base_score * 0.5

            # Clean up query and scheme name for better matching
            clean_query = query_lower.replace("-", " ")
            clean_scheme = (
                scheme_name.replace("-", " ")
                .replace(" direct growth", "")
                .replace(" fund", "")
                .strip()
            )

            # Scheme Name Match: If the core scheme name is mentioned in the query
            # e.g., clean_scheme = "hdfc mid cap", clean_query = "what is the expense ratio of hdfc mid cap"
            if clean_scheme and clean_scheme in clean_query:
                final_score += 0.3
            # Partial match (e.g., matching "nifty 50" specifically instead of "nifty next 50")
            elif (
                "nifty 50" in clean_query
                and "nifty 50" in clean_scheme
                and "next" not in clean_query
                and "next" in clean_scheme
            ):
                # Penalize if they meant Nifty 50 but we retrieved Nifty Next 50
                final_score -= 0.2
            elif "nifty next 50" in clean_query and "nifty next 50" in clean_scheme:
                final_score += 0.3

            # Section Relevance:
            # Simple heuristic: if query contains words like "expense", "nav", "sip", "fee" -> boost fund_details
            # If query contains "about", "who", "what is", "manager" -> boost about_fund
            if section == "fund_details":
                fund_keywords = [
                    "expense",
                    "ratio",
                    "nav",
                    "sip",
                    "fee",
                    "load",
                    "minimum",
                    "rating",
                    "benchmark",
                    "size",
                    "aum",
                ]
                if any(kw in query_lower for kw in fund_keywords):
                    final_score += 0.2
            elif section == "about_fund":
                about_keywords = [
                    "manager",
                    "about",
                    "who manages",
                    "launch",
                    "objective",
                ]
                if any(kw in query_lower for kw in about_keywords):
                    final_score += 0.2

            reranked.append((doc, final_score))

        # Sort by descending final score
        reranked.sort(key=lambda x: x[1], reverse=True)

        # Return top_k
        return reranked[: self.top_k]
