import os
import sys
import unittest

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.retriever import Retriever
from src.rag.reranker import ReRanker


class TestRAGRetrieval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Assumes ChromaDB has been populated by the ingestion script
        cls.retriever = Retriever(
            db_dir="data/chroma_db", top_k=5, similarity_threshold=0.3
        )
        cls.reranker = ReRanker(top_k=3)

    def run_query_test(self, query, expected_scheme_snippet, expected_section):
        print(f"\nQuery: '{query}'")
        raw_results = self.retriever.retrieve(query)
        self.assertTrue(len(raw_results) > 0, "Retriever returned no results.")

        reranked_results = self.reranker.rerank(query, raw_results)
        self.assertTrue(len(reranked_results) > 0, "Reranker returned no results.")

        top_doc, score = reranked_results[0]
        scheme_name = top_doc.metadata.get("scheme_name", "")
        section = top_doc.metadata.get("section", "")

        print(
            f"Top Result -> Scheme: '{scheme_name}', Section: '{section}', Score: {score:.4f}"
        )

        self.assertIn(
            expected_scheme_snippet.lower().replace("-", " "),
            scheme_name.lower().replace("-", " "),
        )
        self.assertEqual(expected_section, section)

    def test_expense_ratio_query(self):
        self.run_query_test(
            "What is the expense ratio of HDFC Mid-Cap Fund?",
            "HDFC Mid-Cap",
            "fund_details",
        )

    def test_exit_load_query(self):
        self.run_query_test(
            "Exit load for HDFC Small Cap Fund", "HDFC Small Cap", "fund_details"
        )

    def test_sip_amount_query(self):
        # We need to make sure the expected snippet actually matches the scheme name stored
        self.run_query_test(
            "Minimum SIP amount for HDFC Nifty 50 Index Fund",
            "HDFC Nifty 50 Index",
            "fund_details",
        )

    def test_risk_level_query(self):
        # In our optimized structure, the risk level ("Very High risk") is inside the about_fund section.
        self.run_query_test(
            "What is the risk level of HDFC Balanced Advantage?",
            "HDFC Balanced Advantage",
            "about_fund",
        )


if __name__ == "__main__":
    unittest.main()
