from .pii_detector import PIIDetector


class QueryClassifier:
    def __init__(self):
        self.pii_detector = PIIDetector()
        self.advisory_keywords = [
            "should i invest",
            "recommend",
            "suggest",
            "which is better",
            "which fund is better",
            "compare",
            "vs",
            "better than",
            "best fund",
            "worth investing",
            "will it go up",
            "future returns",
            "expected growth",
            "good returns",
            "what do you think",
            "is it good",
            "is it safe",
            "guaranteed returns",
            "how much return",
            "profit",
            "is better",
            "tomorrow",
            "next week",
            "prediction",
        ]

    def classify_query(self, query: str) -> str:
        """
        Classify queries as FACTUAL, ADVISORY, or PII_DETECTED.
        """
        # Step 1: Check for PII
        if self.pii_detector.detect_pii(query):
            return "PII_DETECTED"

        # Step 2: Check for advisory intent
        query_lower = query.lower()
        for keyword in self.advisory_keywords:
            if keyword in query_lower:
                return "ADVISORY"

        # Step 3: Default to factual
        return "FACTUAL"
