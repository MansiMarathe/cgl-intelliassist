import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st
from retrieval.retriever import load_vector_store, retrieve_chunks
from llm.prompt_template import build_prompt
from llm.response_generator import generate_answer


st.set_page_config(page_title="SSC CGL 2026 Assistant", page_icon="📄")

st.title("📄 SSC CGL 2026 RAG Assistant")
st.write("Ask any question about the SSC CGL 2026 exam notification — eligibility, fees, syllabus, dates, etc.")


@st.cache_resource
def get_vector_store():
    """
    Loads the FAISS vector store once and caches it across reruns,
    so we don't reload the embedding model on every question.
    """
    return load_vector_store()


vector_store = get_vector_store()

query = st.text_input("Your question:")

if query:
    with st.spinner("Searching document and generating answer..."):
        chunks = retrieve_chunks(query, vector_store, k=4)
        prompt = build_prompt(query, chunks)
        answer = generate_answer(prompt)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("View source chunks used"):
        for i, chunk in enumerate(chunks, start=1):
            st.markdown(f"**Source {i}:**")
            st.text(chunk.page_content[:400])
            st.markdown("---")