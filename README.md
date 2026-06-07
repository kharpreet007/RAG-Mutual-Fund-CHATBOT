# HDFC Mutual Fund FAQ Assistant

An AI-powered, facts-only assistant capable of answering questions regarding 19 supported HDFC Mutual Fund schemes. The system utilizes Retrieval-Augmented Generation (RAG) coupled with extensive guardrails to ensure accuracy, safety, and strict compliance with financial regulations.

> ⚠️ **Facts-only. No investment advice.** This application enforces strict guardrails to refuse any advisory or predictive queries.

## Architecture Overview

The system is composed of two primary components:

### 1. FastAPI Backend & RAG Pipeline
- **Scraping & Ingestion**: Offline pipeline (`src/ingestion`) that scrapes Groww.in URLs for the 19 supported schemes, chunks the HTML into plain text, and generates semantic embeddings using the `BAAI/bge-small-en-v1.5` HuggingFace model.
- **Vector Storage**: Uses ChromaDB to store and retrieve document embeddings locally.
- **Guardrails**: Custom `QueryClassifier` and `PIIDetector` components block Personal Identifiable Information (PAN, Aadhaar, phone numbers) and detect advisory or predictive language (e.g. "Should I invest?", "What will the NAV be tomorrow?").
- **Generation**: Powered by Groq's blazing-fast `llama-3.1-8b-instant` LLM with temperature `0.0` to ensure highly deterministic, factual responses based strictly on the retrieved context.

### 2. Next.js Frontend
- **Framework**: Next.js 14 App Router, built with Tailwind CSS v3.
- **Design System**: Implements a sleek dark-mode UI featuring glassmorphism elements (`backdrop-blur`), deep floating shadows, and interactive quick-action pill buttons.
- **Interaction**: Features a persistent left sidebar containing all 19 supported schemes. Selecting a scheme provides quick-action prompts (e.g., NAV, Expense Ratio, Exit Load) that execute end-to-end RAG queries seamlessly.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js v18+
- A free [Groq API Key](https://console.groq.com/keys)

### Backend Setup

1. **Environment Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Copy the example config and add your Groq API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GROQ_API_KEY=gsk_your_api_key_here
   ```

3. **Run the Ingestion Pipeline** (Optional, database is pre-built in `data/chroma_db`):
   ```bash
   python run_scrape.py
   ```

4. **Start the FastAPI Server**:
   ```bash
   uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Development Server**:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`.

## AMC Selection Rationale

**HDFC Mutual Fund** was selected as the target AMC for this project due to:
1. High search volume and popularity of their flagship funds (e.g., HDFC Balanced Advantage, HDFC Mid-Cap Opportunities).
2. Consistent availability of structured, well-documented scheme information across mutual fund aggregators (like Groww), making scraping and RAG retrieval highly effective.

## Known Limitations
- The system only supports the 19 specifically enumerated HDFC schemes. Queries regarding other AMCs or unsupported HDFC schemes will gracefully fail.
- As the system relies on statically scraped HTML from Groww, extremely real-time data (like intraday NAV fluctuations) may not be perfectly accurate until the ingestion pipeline is re-run.

## License
Proprietary / Internal Use Only.
