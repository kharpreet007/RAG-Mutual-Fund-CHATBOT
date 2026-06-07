import os
import json
import logging
from datetime import datetime

from langchain_chroma import Chroma
from .chunker import DataChunker
from .embedder import Embedder

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class IngestionOrchestrator:
    def __init__(self):
        self.processed_dir = "data/processed"
        self.db_dir = "data/chroma_db"
        self.metadata_registry_path = "data/metadata.json"

        logging.info("Initializing Chunking and Embedding models...")
        self.chunker = DataChunker()
        self.embedder = Embedder()

        # Ensure directories exist
        os.makedirs(self.db_dir, exist_ok=True)

    def run(self):
        logging.info("Starting ingestion pipeline...")

        all_docs = []
        registry = []
        failures = []

        # We assume scraping and structuring has already run,
        # or we just process whatever is in data/processed
        if not os.path.exists(self.processed_dir):
            logging.error(f"Directory {self.processed_dir} does not exist!")
            return

        files = [f for f in os.listdir(self.processed_dir) if f.endswith(".json")]
        logging.info(f"Found {len(files)} scheme JSON files to process.")

        for filename in files:
            filepath = os.path.join(self.processed_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                docs = self.chunker.chunk_structured_data(data)
                all_docs.extend(docs)

                # Append to metadata registry
                for doc in docs:
                    registry.append(doc.metadata)

                logging.info(f"Processed {filename}: generated {len(docs)} chunks.")
            except Exception as e:
                logging.error(f"Failed to process {filename}: {e}")
                failures.append(filename)

        if not all_docs:
            logging.warning("No documents were generated. Aborting DB ingestion.")
            return

        logging.info(
            f"Total chunks generated: {len(all_docs)}. Initializing ChromaDB ingestion..."
        )

        # Ingest into ChromaDB
        # The persist_directory tells Chroma to save data to disk
        vectorstore = Chroma.from_documents(
            documents=all_docs,
            embedding=self.embedder.get_embeddings(),
            persist_directory=self.db_dir,
        )

        logging.info("Successfully saved vectors to ChromaDB.")

        # Save Metadata Registry
        with open(self.metadata_registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

        logging.info(f"Saved metadata registry to {self.metadata_registry_path}")

        # Print Summary
        print("\n" + "=" * 40)
        print("INGESTION SUMMARY")
        print("=" * 40)
        print(f"Total Schemes Processed: {len(files) - len(failures)}")
        print(f"Total Chunks Generated:  {len(all_docs)}")
        print(f"Total Failures:          {len(failures)}")
        if failures:
            print("Failed files:", failures)
        print("=" * 40 + "\n")


if __name__ == "__main__":
    # If run as standalone, ensure working directory is correct
    # We expect to run this from the backend folder
    orchestrator = IngestionOrchestrator()
    orchestrator.run()
