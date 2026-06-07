import json
from datetime import datetime
from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataChunker:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk_structured_data(
        self, data: dict, scrape_date: str = None
    ) -> List[Document]:
        """
        Takes the cleaned structured JSON data and turns it into Langchain Documents.
        Since the data is now structured, we can create semantic chunks explicitly
        (e.g., one chunk for fast facts, and chunk(s) for the about text).
        """
        documents = []
        scheme_name = data.get("scheme_name", "Unknown Scheme")
        url = data.get("url", "")
        scheme_slug = url.split("/")[-1] if url else "unknown-slug"

        # Use provided scrape_date or default to today
        if not scrape_date:
            scrape_date = datetime.now().strftime("%Y-%m-%d")

        # We don't have explicit category in the scraped JSON right now, but we can default or parse it if we had it
        category = "Mutual Fund"

        chunk_index = 1

        # 1. Chunk for Fast Facts (Fund Details)
        # We explicitly format the key-value pairs into a highly readable text block for the LLM
        facts_text = f"Scheme Name: {scheme_name}\n"
        if data.get("expense_ratio"):
            facts_text += f"Expense Ratio: {data['expense_ratio']}\n"
        if data.get("exit_load"):
            facts_text += f"Exit Load: {data['exit_load']}\n"
        if data.get("aum"):
            facts_text += f"Fund Size (AUM): {data['aum']}\n"
        if data.get("nav"):
            facts_text += f"Latest NAV: {data['nav']}\n"
        if data.get("min_sip"):
            facts_text += f"Minimum SIP Investment: {data['min_sip']}\n"
        if data.get("rating"):
            facts_text += f"Rating: {data['rating']}\n"
        if data.get("benchmark"):
            facts_text += f"Benchmark Index: {data['benchmark']}\n"
        if data.get("launch_date"):
            facts_text += f"Launch Date: {data['launch_date']}\n"
        if data.get("fund_manager"):
            facts_text += f"Fund Manager: {data['fund_manager']}\n"

        facts_doc = Document(
            page_content=facts_text.strip(),
            metadata={
                "chunk_id": f"{scheme_slug}-{chunk_index}",
                "scheme_name": scheme_name,
                "category": category,
                "source_url": url,
                "section": "fund_details",
                "scrape_date": scrape_date,
            },
        )
        documents.append(facts_doc)
        chunk_index += 1

        # 2. Chunk for the About Text
        # The About text might be slightly longer, so we use the text splitter to be safe.
        about_text = data.get("about_fund", "")
        if about_text:
            # We prefix the about text so the chunk retains context even if split
            prefix = f"About {scheme_name}: "
            about_chunks = self.text_splitter.split_text(about_text)

            for chunk in about_chunks:
                # If the chunk doesn't start with the scheme name, we add it for context
                if not chunk.startswith("About"):
                    chunk = prefix + chunk

                doc = Document(
                    page_content=chunk,
                    metadata={
                        "chunk_id": f"{scheme_slug}-{chunk_index}",
                        "scheme_name": scheme_name,
                        "category": category,
                        "source_url": url,
                        "section": "about_fund",
                        "scrape_date": scrape_date,
                    },
                )
                documents.append(doc)
                chunk_index += 1

        return documents


if __name__ == "__main__":
    import os

    chunker = DataChunker()
    sample_json_path = (
        "backend/data/processed/hdfc-balanced-advantage-fund-direct-growth.json"
    )

    if os.path.exists(sample_json_path):
        with open(sample_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        docs = chunker.chunk_structured_data(data)

        print(f"Generated {len(docs)} chunks for {data['scheme_name']}:\n")
        for i, doc in enumerate(docs):
            print(f"--- Chunk {i+1} [Section: {doc.metadata['section']}] ---")
            print(doc.page_content)
            print("Metadata:", json.dumps(doc.metadata, indent=2))
            print("-" * 50)
