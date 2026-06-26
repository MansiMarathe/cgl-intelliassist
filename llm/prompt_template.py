def build_prompt(query, retrieved_chunks):
    """
    Builds a prompt that combines the user's query with retrieved
    context chunks, instructing the LLM to answer ONLY from the
    given context, formatted clearly with markdown.
    """
    context = "\n\n---\n\n".join(
        [chunk.page_content for chunk in retrieved_chunks]
    )

    prompt = f"""You are a helpful assistant that explains the SSC CGL 2026 exam notification to candidates in simple, easy-to-understand language.

INSTRUCTIONS:
- Answer using ONLY the information in the context below.
- If the answer is not present in the context, say "I couldn't find this information in the provided document. You may want to check the official notification for this detail."
- Format your answer using Markdown:
  - Use **bold** for important terms, numbers, and dates.
  - Use bullet points (-) for lists of items, criteria, or steps.
  - Use short paragraphs for explanations.
  - Break the answer into sections with headings (##) if the topic has multiple parts (e.g., eligibility criteria, fee details, exemptions).
- Keep the language simple and avoid jargon. Explain any technical/government terms briefly.
- Be thorough but not repetitive.

Context:
{context}

Question: {query}

Answer (in Markdown):"""

    return prompt