import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_into_sections(text):
    """
    Splits the cleaned document text into major numbered sections
    (e.g., '2. Details of the Posts', '5. Age limit', '13. Scheme of Examination')
    based on top-level numbering pattern at the start of a line.
    """
    # Pattern matches lines starting with "1.", "2.", ... "20." followed by a space and capital letter
    section_pattern = re.compile(r'\n(?=\d{1,2}\.\s+[A-Z])')

    sections = section_pattern.split(text)

    # Clean up each section
    sections = [s.strip() for s in sections if s.strip()]

    return sections


def chunk_sections(sections, chunk_size=1000, chunk_overlap=150):
    """
    Takes large sections and splits them further into smaller chunks
    using a recursive character splitter, while keeping smaller
    sections intact as single chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    final_chunks = []

    for section in sections:
        if len(section) <= chunk_size:
            final_chunks.append(section)
        else:
            sub_chunks = splitter.split_text(section)
            final_chunks.extend(sub_chunks)

    return final_chunks

def chunk_sections(sections, chunk_size=1000, chunk_overlap=150, min_chunk_size=30):
    """
    Takes large sections and splits them further into smaller chunks
    using a recursive character splitter, while keeping smaller
    sections intact as single chunks. Drops chunks that are too
    small to carry meaningful information.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    final_chunks = []

    for section in sections:
        if len(section) <= chunk_size:
            final_chunks.append(section)
        else:
            sub_chunks = splitter.split_text(section)
            final_chunks.extend(sub_chunks)

    # Filter out tiny, meaningless chunks
    final_chunks = [c for c in final_chunks if len(c.strip()) >= min_chunk_size]

    return final_chunks


# Quick test when running this file directly
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from ingestion.loader import load_pdf, clean_text

    pdf_path = "data/Notice_of_adv_cgl_2026.pdf"

    text = load_pdf(pdf_path)
    cleaned = clean_text(text)

    sections = split_into_sections(cleaned)
    print(f"Number of major sections found: {len(sections)}")

    chunks = chunk_sections(sections)
    print(f"Total chunks after splitting: {len(chunks)}")

    print("\n--- Sample: First section's start ---")
    print(sections[0][:200])

    print("\n--- Sample: A chunk from the middle ---")
    print(chunks[len(chunks)//2][:400])

    print("\n--- Chunk size distribution ---")
    sizes = [len(c) for c in chunks]
    print(f"Min: {min(sizes)}, Max: {max(sizes)}, Avg: {sum(sizes)//len(sizes)}")