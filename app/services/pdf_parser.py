"""Turn an uploaded PDF into plain text."""
import io
from pypdf import PdfReader


class CVInputError(Exception):
    """The user's input is unusable (bad file, empty text, too long...)."""

def parse_pdf(data: bytes) -> str:
    try: 
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception:
        raise CVInputError("Could not read this file. Please upload a valid PDF.")

    text = "\n".join(pages).strip()

    if not text:
        raise CVInputError("No text found in the PDF. Please paste your CV text instead.")

    return text