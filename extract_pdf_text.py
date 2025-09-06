import pdfplumber

def extract_text_from_pdf(pdf_source):
    """
    Extracts text from a PDF file (path or file-like object).
    Keeps the raw text as in the sample PDFs.
    """
    if isinstance(pdf_source, str):  # file path
        pdf = pdfplumber.open(pdf_source)
    else:  # uploaded file-like object
        pdf = pdfplumber.open(pdf_source)

    text_parts = []
    for page in pdf.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text.strip())

    pdf.close()
    return "\n".join(text_parts)
