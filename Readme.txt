# JSON → PDF / DOCX Converter API

A FastAPI service that accepts JSON data (and optional images) and generates professional PDF or DOCX reports.  
Internally, the service transforms JSON into styled HTML, then renders it with **wkhtmltopdf** (for PDFs) or **python-docx** (for DOCX).

---

## Features
- Accepts **JSON data** as inline text or uploaded file.
- Embeds an optional image (PNG/JPEG recommended).
- Outputs clean, paragraph-based reports instead of raw tables.
- Two output formats: **PDF** or **DOCX**.

---

## Installation

### 1. Clone repo & install dependencies
```bash
uv sync
Your pyproject.toml must include:

toml
Copy code
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "pdfkit",
  "python-docx",
  "python-multipart",
  "python-dotenv"
]
2. Install wkhtmltopdf system binary
Windows: Download, install to
C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
Add the bin folder to your PATH or set in .env:

ini
Copy code
WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
Linux (Debian/Ubuntu):

bash
Copy code
sudo apt-get update && sudo apt-get install -y wkhtmltopdf
Running
bash
Copy code
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
Visit http://127.0.0.1:8000/docs for interactive API docs.

API Endpoints
GET /healthz
Check if service and wkhtmltopdf are available.

POST /render
Generate a report.

Form-data fields
json_text (string) — JSON content inline (alternative to text file).

text (file) — JSON file upload.

image (file, optional) — PNG or JPEG to embed. (SVG is only supported in PDF, not DOCX).

output (string, required) — "pdf" or "docx".

title (string, optional) — Report title.

JSON Format
Recommended schema
json
Copy code
{
  "title": "Quarterly Review",
  "sections": [
    {
      "heading": "Executive Summary",
      "type": "paragraph",
      "text": "This quarter we saw growth in all regions..."
    },
    {
      "heading": "KPIs",
      "type": "list",
      "items": ["Revenue +12%", "New hires: 10", "Customer churn -3%"]
    },
    {
      "heading": "Financials",
      "type": "table",
      "rows": [["Q1", "$1M"], ["Q2", "$1.2M"], ["Q3", "$1.3M"]]
    }
  ]
}
sections is an array of objects.

type can be:

"paragraph" → renders <p>…</p>

"list" → renders <ul><li>…</li></ul>

"table" → renders <table>…</table>

Flat dict fallback
If you send a simple JSON dict without sections, keys will be rendered as headings/paragraphs/tables depending on prefix (h1, h2:, p:, list:, table:).

Image Guidelines
Supported formats: PNG, JPEG (both PDF and DOCX).

SVG: works in PDF but not in DOCX (will raise error).

Images are scaled to page width (max-width:100%) and centered.

Keep file size reasonable (<1 MB recommended).

Examples
1. JSON text + PDF
powershell
Copy code
Invoke-WebRequest -Method POST "http://127.0.0.1:8000/render" `
  -Form @{
    "json_text" = '{"title":"My Report","sections":[{"heading":"Intro","type":"paragraph","text":"Hello"}]}'
    "output"    = "pdf"
    "title"     = "Demo Report"
  } -OutFile demo.pdf
2. JSON file + image + DOCX
powershell
Copy code
Invoke-WebRequest -Method POST "http://127.0.0.1:8000/render" `
  -Form @{
    "text"   = Get-Item ".\text.json"
    "image"  = Get-Item ".\chart.png"
    "output" = "docx"
    "title"  = "Report With Image"
  } -OutFile demo.docx
Notes
For production: bundle wkhtmltopdf into your Dockerfile to avoid local install issues.

Always validate input JSON before sending to /render.