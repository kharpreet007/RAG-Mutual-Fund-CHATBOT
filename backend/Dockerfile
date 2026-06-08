FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the HuggingFace embedding model at build time so it doesn't download on every startup
RUN python -c "from langchain_community.embeddings import SentenceTransformerEmbeddings; SentenceTransformerEmbeddings(model_name='BAAI/bge-small-en-v1.5')"

# Copy application code
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
