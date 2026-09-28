from io import BytesIO

from docx import Document
from pypdf import PdfReader

from parsers.text_cleaner import clean_text


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract and clean text from a PDF file."""
    reader = PdfReader(BytesIO(file_bytes))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    raw_text = "\n".join(pages)

    return clean_text(raw_text)


def extract_docx_text(file_bytes: bytes) -> str:
    """Extract and clean text from a DOCX file."""
    document = Document(BytesIO(file_bytes))

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    raw_text = "\n".join(paragraphs)

    return clean_text(raw_text)


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text based on the uploaded file extension."""
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file_bytes)

    if filename.endswith(".docx"):
        return extract_docx_text(file_bytes)

    raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")