import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.generator import ResponseGenerator
from langchain_core.documents import Document


class TestGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to test validation independent of the actual LLM call to save API calls
        # Set a dummy API key so ChatGroq doesn't crash on initialization
        os.environ["GROQ_API_KEY"] = "dummy_key_for_tests"
        cls.generator = ResponseGenerator(model_name="test-model")

    def test_validate_response_valid(self):
        answer = "The expense ratio is 0.75%. Source: https://groww.in. Last updated from sources: 2026-06-05."
        result = self.generator.validate_response(answer)
        self.assertTrue(result["valid"], "Valid answer should pass validation")
        self.assertEqual(len(result["issues"]), 0)

    def test_validate_response_missing_footer(self):
        answer = "The expense ratio is 0.75%. Source: https://groww.in."
        result = self.generator.validate_response(answer)
        self.assertFalse(result["valid"])
        self.assertIn("Missing 'Last updated' footer", result["issues"])

    def test_validate_response_advisory_language(self):
        answer = "I recommend you should invest in this fund. Last updated from sources: 2026-06-05."
        result = self.generator.validate_response(answer)
        self.assertFalse(result["valid"])
        self.assertTrue(any("advisory language" in issue for issue in result["issues"]))

    def test_validate_response_too_long(self):
        # Over 4 sentences
        answer = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five. Last updated from sources: 2026-06-05."
        result = self.generator.validate_response(answer)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("Exceeds 3-sentence limit" in issue for issue in result["issues"])
        )

    @patch("src.rag.generator.ChatGroq")
    def test_generate_out_of_scope(self, MockChatGroq):
        # Setup mock
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "I don't have this information in my sources."
        mock_llm.invoke.return_value = mock_response

        # We patch the chain directly for simplicity
        generator = ResponseGenerator()
        generator.chain = mock_llm

        doc = Document(
            page_content="Some unrelated text",
            metadata={"source_url": "url", "scrape_date": "date"},
        )
        answer = generator.generate("What is the capital of France?", [doc])

        self.assertEqual(answer, "I don't have this information in my sources.")


if __name__ == "__main__":
    unittest.main()
