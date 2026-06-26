import os
import sys
from dotenv import load_dotenv
from groq import Groq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(prompt, model="llama-3.3-70b-versatile"):
    """
    Sends the prompt to Groq's LLM and returns the generated answer.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content


# Quick test when running this file directly
if __name__ == "__main__":
    from retrieval.retriever import load_vector_store, retrieve_chunks
    from llm.prompt_template import build_prompt

    print("Loading vector store...")
    vector_store = load_vector_store()

    query = "What is the application fee and who is exempted from paying it?"

    print(f"\nQuery: {query}")

    chunks = retrieve_chunks(query, vector_store, k=4)

    prompt = build_prompt(query, chunks)

    print("\nGenerating answer...")
    answer = generate_answer(prompt)

    print("\n--- ANSWER ---")
    print(answer)