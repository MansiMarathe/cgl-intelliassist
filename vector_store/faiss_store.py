import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.vectorstores import FAISS
from ingestion.loader import load_pdf, clean_text
from ingestion.chunker import split_into_sections, chunk_sections
from embeddings.embedding_model import get_embedding_model


def build_vector_store(pdf_path, save_path="vector_store/faiss_index"):
    """
    Full pipeline: load PDF -> clean -> chunk -> embed -> save FAISS index.
    """
    print("Loading PDF...")
    text = load_pdf(pdf_path)
    cleaned = clean_text(text)

    print("Chunking text...")
    sections = split_into_sections(cleaned)
    chunks = chunk_sections(sections)
    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")
    embedder = get_embedding_model()

    print("Creating FAISS index (this embeds all chunks)...")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embedder)

    print(f"Saving index to {save_path} ...")
    vector_store.save_local(save_path)

    print("Done.")
    return vector_store


# Quick test when running this file directly
if __name__ == "__main__":
    pdf_path = "data/Notice_of_adv_cgl_2026.pdf"
    build_vector_store(pdf_path)