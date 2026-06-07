class RefusalHandler:
    def __init__(self):
        self.responses = {
            "PII_DETECTED": "I detected potential personal information in your query. For your privacy and security, I cannot process queries containing PAN, Aadhaar, phone numbers, or email addresses. Facts-only. No investment advice.",
            "ADVISORY": "I am an AI assistant designed strictly to provide factual information about HDFC Mutual Fund schemes. I cannot provide investment advice, recommendations, or forward-looking predictions. Please consult a certified financial advisor for investment decisions. Facts-only. No investment advice.",
        }

    def get_refusal(self, classification: str) -> str:
        """
        Returns a polite refusal response based on the query classification.
        If the classification is FACTUAL, returns an empty string.
        """
        return self.responses.get(classification, "")
