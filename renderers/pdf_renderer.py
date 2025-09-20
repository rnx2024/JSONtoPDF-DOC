import pdfkit
from config import PDFKIT_CONFIG, PDF_OPTIONS

def html_to_pdf_bytes(html: str) -> bytes:
    return pdfkit.from_string(
        html,
        False,
        configuration=PDFKIT_CONFIG,
        options=PDF_OPTIONS,
    )
