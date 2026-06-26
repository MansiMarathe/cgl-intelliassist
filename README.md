# SSC CGL 2026 RAG Assistant

An AI-powered information assistant for the SSC CGL 2026 exam notification, built using Retrieval Augmented Generation (RAG).

## Tech Stack
- **Backend**: Python, FastAPI, LangChain, FAISS, HuggingFace Embeddings, Groq API (Llama 3.3-70b)
- **Frontend**: Node.js, Express
- **Pipeline**: PDF Loader → Text Cleaner → Chunker → Embeddings → FAISS Vector Store → LLM

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Add `.env` with `GROQ_API_KEY=your_key`
3. Build vector store: `python vector_store/faiss_store.py`
4. Run backend: `python -m uvicorn api.main:app --host 0.0.0.0 --port 8000`
5. Run frontend: `cd frontend && node server.js`