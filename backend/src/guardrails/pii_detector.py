import re


class PIIDetector:
    def __init__(self):
        self.patterns = {
            "pan": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
            "aadhaar": r"[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}",
            "phone": r"(\+91)?[6-9][0-9]{9}",
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        }

    def detect_pii(self, text: str) -> bool:
        """
        Returns True if any PII pattern is matched in the input text.
        """
        for name, pattern in self.patterns.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True
        return False
