import os
import sys
import unittest

# Ensure backend directory is in path and set dummy env vars
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "dummy_key_for_tests")

from fastapi.testclient import TestClient
from src.app import app, init_components


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize components and create the test client."""
        init_components()
        cls.client = TestClient(app)

    def test_health_check(self):
        """Test 1: GET /health returns 200 with status ok."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")

    def test_list_schemes(self):
        """Test 6: GET /schemes returns 200 with array of scheme names."""
        response = self.client.get("/schemes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("schemes", data)
        self.assertIn("count", data)
        self.assertEqual(data["count"], 19)
        # Verify each scheme has a name
        for scheme in data["schemes"]:
            self.assertIn("scheme_name", scheme)
            self.assertTrue(len(scheme["scheme_name"]) > 0)

    def test_empty_query(self):
        """Test 5: POST /ask with empty query returns status 'error'."""
        response = self.client.post("/ask", json={"query": ""})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "error")

    def test_advisory_query(self):
        """Test 3: POST /ask with advisory query returns status 'refused'."""
        response = self.client.post(
            "/ask", json={"query": "Should I invest in HDFC Mid-Cap Fund?"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "refused")
        self.assertIn("educational_link", data)

    def test_pii_query(self):
        """Test 4: POST /ask with PII returns status 'refused'."""
        response = self.client.post("/ask", json={"query": "My PAN is ABCDE1234F"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "refused")
        self.assertIn("educational_link", data)

    def test_factual_query(self):
        """Test 2: POST /ask with factual query returns status 'success'."""
        response = self.client.post(
            "/ask", json={"query": "What is the expense ratio of HDFC Small Cap Fund?"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("answer", data)
        self.assertIn("citation", data)
        # The disclaimer should always be present
        self.assertIn("disclaimer", data)


if __name__ == "__main__":
    unittest.main()
