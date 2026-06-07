import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama3-8b-8192"
CHROMA_PERSIST_DIR = "data/chroma_db"
COLLECTION_NAME = "hdfc_mutual_funds"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5
TOP_N_RERANK = 3
SIMILARITY_THRESHOLD = 0.7
