from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Loads and returns a HuggingFace embedding model.
    'all-MiniLM-L6-v2' is small, fast, and runs locally (no API key needed).
    It converts text into 384-dimensional vectors.
    """
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return model


# Quick test when running this file directly
if __name__ == "__main__":
    embedder = get_embedding_model()

    sample_text = "What is the age limit for Junior Statistical Officer?"

    vector = embedder.embed_query(sample_text)

    print(f"Sample text: {sample_text}")
    print(f"Embedding vector length: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")