import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from retrieval.retriever import load_vector_store, retrieve_chunks
from llm.prompt_template import build_prompt
from llm.response_generator import generate_answer


app = FastAPI(title="SSC CGL 2026 RAG Assistant API")

# Allow the Node.js frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading vector store... (one-time setup)")
vector_store = load_vector_store()
print("Vector store loaded. API ready.")


class QueryRequest(BaseModel):
    question: str


class SourceChunk(BaseModel):
    content: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


@app.get("/")
def health_check():
    return {"status": "ok", "message": "SSC CGL 2026 RAG API is running"}


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    chunks = retrieve_chunks(request.question, vector_store, k=4)

    prompt = build_prompt(request.question, chunks)
    answer = generate_answer(prompt)

    sources = [SourceChunk(content=chunk.page_content[:400]) for chunk in chunks]

    return QueryResponse(answer=answer, sources=sources)