from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


class HTMLCleaner:
    """Utility class to extract and clean factual text from raw HTML."""

    @staticmethod
    def clean_html(raw_html: str) -> str:
        """Cleans raw HTML and extracts relevant factual text.

        Args:
            raw_html (str): The raw HTML string fetched from the scraper.

        Returns:
            str: Cleaned, space-normalized text content.
        """
        if not raw_html:
            return ""

        soup = BeautifulSoup(raw_html, "html.parser")

        # Decompose elements that usually don't contain factual scheme content
        tags_to_remove = [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "svg",
            "button",
            "iframe",
            "form",
            "input",
            "meta",
        ]
        for tag in soup(tags_to_remove):
            tag.decompose()

        # Remove elements by class names indicating boilerplate (Groww-specific UI)
        elements_to_remove = []
        for element in soup.find_all(["div", "section", "ul", "li", "a"]):
            classes = element.get("class")
            if classes:
                if isinstance(classes, list):
                    class_str = " ".join(classes).lower()
                else:
                    class_str = str(classes).lower()

                # Check for common boilerplate classes
                if any(
                    x in class_str
                    for x in [
                        "header",
                        "footer",
                        "nav",
                        "sidebar",
                        "menu",
                        "dropdown",
                        "banner",
                        "disclaimer",
                        "quicklink",
                    ]
                ):
                    elements_to_remove.append(element)

        # Decompose matched boilerplate elements
        for element in elements_to_remove:
            try:
                element.decompose()
            except Exception:
                pass

        # Try to target the main content area if possible to reduce noise.
        # Groww usually puts content in divs. We'll extract everything in body.
        body = soup.body if soup.body else soup

        # Get text, separating blocks with a space
        text = body.get_text(separator=" ", strip=True)

        # Normalize whitespace (replace multiple spaces/newlines with a single space)
        text = re.sub(r"\s+", " ", text)

        return text.strip()
