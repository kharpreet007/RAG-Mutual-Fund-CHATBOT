import os
import sys
import unittest

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.guardrails.classifier import QueryClassifier
from src.guardrails.refusal import RefusalHandler
from src.guardrails.pii_detector import PIIDetector


class TestGuardrails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.classifier = QueryClassifier()
        cls.refusal = RefusalHandler()
        cls.pii = PIIDetector()

    def test_classifier_cases(self):
        test_cases = [
            ("What is the expense ratio of HDFC Mid-Cap Fund?", "FACTUAL"),
            ("Should I invest in HDFC Small Cap Fund?", "ADVISORY"),
            ("Which fund is better, HDFC Mid-Cap or Small Cap?", "ADVISORY"),
            ("My PAN is ABCDE1234F, check my fund", "PII_DETECTED"),
            ("Call me at 9876543210", "PII_DETECTED"),
            ("What is the exit load?", "FACTUAL"),
            ("Will HDFC Equity Fund give good returns?", "ADVISORY"),
            ("My email is example@email.com", "PII_DETECTED"),
            ("Here is my Aadhaar: 1234 5678 9012", "PII_DETECTED"),
        ]

        for query, expected_class in test_cases:
            classification = self.classifier.classify_query(query)
            self.assertEqual(
                classification, expected_class, f"Failed on query: '{query}'"
            )

    def test_refusal_handler(self):
        pii_response = self.refusal.get_refusal("PII_DETECTED")
        adv_response = self.refusal.get_refusal("ADVISORY")
        fact_response = self.refusal.get_refusal("FACTUAL")

        self.assertIn("personal information", pii_response.lower())
        self.assertIn("investment advice", adv_response.lower())
        self.assertEqual(fact_response, "")


if __name__ == "__main__":
    unittest.main()
