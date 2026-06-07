import os
from langchain_huggingface import HuggingFaceEmbeddings


class Embedder:
    def __init__(self, model_name: str = None, device: str = "cpu"):
        """
        Initialize the HuggingFace BGE Embeddings model.
        BGE-small is highly optimized for retrieval tasks and runs locally without any API calls.
        """
        # Suppress symlink warnings from huggingface_hub
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

        self.model_name = model_name or os.getenv(
            "EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5"
        )
        self.device = device
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs={
                "normalize_embeddings": True
            },  # True yields cosine similarity == dot product
        )

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Returns the underlying langchain embeddings object.
        """
        return self.embeddings


if __name__ == "__main__":
    # Test script to verify the embedder loads and encodes properly
    import time

    print("Initializing Embedder (this may download model weights on first run)...")
    start = time.time()
    embedder = Embedder()
    emb_obj = embedder.get_embeddings()
    end = time.time()

    print(f"Embedder initialized in {end - start:.2f} seconds.")

    test_text = (
        "HDFC Balanced Advantage Fund Direct Growth is a Hybrid Mutual Fund Scheme."
    )
    print(f"\nEmbedding test text: '{test_text}'")

    start = time.time()
    vector = emb_obj.embed_query(test_text)
    end = time.time()

    print(f"Embedding generated in {end - start:.4f} seconds.")
    print(f"Vector dimension: {len(vector)}")
    print(f"Sample values (first 5): {vector[:5]}")
