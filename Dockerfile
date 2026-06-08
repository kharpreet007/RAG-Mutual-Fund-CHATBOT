# Root Dockerfile specifically for Railway Deployment
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the HuggingFace embedding model at build time
RUN python -c "from langchain_community.embeddings import SentenceTransformerEmbeddings; SentenceTransformerEmbeddings(model_name='BAAI/bge-small-en-v1.5')"

# Copy the backend code into the container
COPY backend/ .

EXPOSE 8000

# Start the FastAPI server using Railway's dynamic PORT
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
