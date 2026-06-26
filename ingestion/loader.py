import re
import pdfplumber

def load_pdf(file_path):
    """
    Loads a PDF and extracts text page by page using pdfplumber.
    Layout-aware extraction works well for this document since it 
    contains tables (vacancy details, pay scales, exam centres).
    """
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        print(f"Total pages found: {len(pdf.pages)}")

        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text


def clean_text(text):
    """
    Removes Hindi (Devanagari script) lines, keeping only English content.
    Also removes page-break artifacts (e.g., 'Page 51 of 132') and
    collapses excessive blank lines.
    """
    cleaned_lines = []

    for line in text.split("\n"):
        # Skip lines that contain Devanagari characters
        if re.search(r'[\u0900-\u097F]', line):
            continue
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # Remove page-break markers like "Page 51 of 132"
    cleaned_text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', cleaned_text)

    # Collapse multiple blank lines into one
    cleaned_text = re.sub(r'\n\s*\n+', '\n\n', cleaned_text)

    return cleaned_text


# Quick test when running this file directly
if __name__ == "__main__":
    pdf_path = "data/Notice_of_adv_cgl_2026.pdf"

    text = load_pdf(pdf_path)
    cleaned = clean_text(text)

    print("\n--- Extraction Summary ---")
    print(f"Raw characters: {len(text)}")
    print(f"Cleaned characters: {len(cleaned)}")

    print("\n--- First 800 characters (cleaned) ---")
    print(cleaned[:800])