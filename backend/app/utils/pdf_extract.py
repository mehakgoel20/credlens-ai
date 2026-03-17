from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    all_text = []
    for page in reader.pages:
        all_text.append(page.extract_text() or "")
    return "\n".join(all_text).strip()
