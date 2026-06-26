import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.vectorstores import FAISS
from embeddings.embedding_model import get_embedding_model


def load_vector_store(index_path="vector_store/faiss_index"):
    """
    Loads a previously saved FAISS index from disk.
    """
    embedder = get_embedding_model()

    vector_store = FAISS.load_local(
        index_path,
        embedder,
        allow_dangerous_deserialization=True  # safe here, since we created this index ourselves
    )

    return vector_store


def retrieve_chunks(query, vector_store, k=4):
    """
    Given a query, returns the top-k most relevant chunks from the index.
    """
    results = vector_store.similarity_search(query, k=k)
    return results


# Quick test when running this file directly
if __name__ == "__main__":
    print("Loading vector store...")
    vector_store = load_vector_store()

    test_queries = [
        "What is the age limit for Junior Statistical Officer?",
        "What is the application fee?",
        "What documents are required for OBC certificate?",
    ]

    for query in test_queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)

        results = retrieve_chunks(query, vector_store, k=2)

        for i, doc in enumerate(results, start=1):
            print(f"\n--- Result {i} ---")
            print(doc.page_content[:400])