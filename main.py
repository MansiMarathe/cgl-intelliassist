import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from retrieval.retriever import load_vector_store, retrieve_chunks
from llm.prompt_template import build_prompt
from llm.response_generator import generate_answer


def get_answer(query, vector_store, k=4):
    """
    Full RAG pipeline for a single query:
    retrieve relevant chunks -> build prompt -> generate answer.
    Returns both the answer and the source chunks used.
    """
    chunks = retrieve_chunks(query, vector_store, k=k)
    prompt = build_prompt(query, chunks)
    answer = generate_answer(prompt)

    return answer, chunks


# Interactive command-line chat loop
if __name__ == "__main__":
    print("Loading vector store... (this may take a few seconds)")
    vector_store = load_vector_store()

    print("\nSSC CGL 2026 RAG Assistant ready! Type 'exit' to quit.\n")

    while True:
        query = input("Your question: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer, chunks = get_answer(query, vector_store)

        print("\n--- ANSWER ---")
        print(answer)

        print("\n--- SOURCES (for verification) ---")
        for i, chunk in enumerate(chunks, start=1):
            print(f"\nSource {i}: {chunk.page_content[:150]}...")

        print("\n" + "="*60 + "\n")