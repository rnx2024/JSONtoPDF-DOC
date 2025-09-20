import os
import pdfkit
from typing import Optional

WKHTMLTOPDF_PATH: Optional[str] = os.getenv("WKHTMLTOPDF_PATH")
PDFKIT_CONFIG = (
    pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    if WKHTMLTOPDF_PATH else None
)

PDF_OPTIONS = {
    "print-media-type": None,
    "enable-local-file-access": None,
    "margin-top": "12mm",
    "margin-right": "12mm",
    "margin-bottom": "16mm",
    "margin-left": "12mm",
    "page-size": "A4",
}
