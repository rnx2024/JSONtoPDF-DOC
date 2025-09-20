Add that `bin` to `PATH` or set in `.env`:
~~~ini
WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
~~~

**Debian/Ubuntu**
~~~bash
sudo apt-get update && sudo apt-get install -y wkhtmltopdf
~~~

sudo apt-get update && sudo apt-get install -y wkhtmltopdf
~~~

---

## Run
~~~bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
~~~
Open `http://127.0.0.1:8000/docs`.

---

## API

### GET `/healthz`

Health check for service and wkhtmltopdf.

### POST `/render`
Generate report.

**Form fields**
- `json_text` *(string)* — inline JSON (alt to file).
- `text` *(file)* — JSON file upload.
- `image` *(file, optional)* — PNG/JPEG. *(SVG only supported for PDF, not DOCX.)*
- `output` *(string, required)* — `"pdf"` or `"docx"`.
- `title` *(string, optional)* — report title.

---

## JSON Format

**Recommended schema**
~~~json
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
~~~

`sections[i].type` is one of:
- `"paragraph"` → `<p>…</p>`
- `"list"` → `<ul><li>…</li></ul>`
- `"table"` → `<table>…</table>`

**Flat dict fallback**  
If no `sections`, a simple dict is rendered by key prefixes: `h1:`, `h2:`, `p:`, `list:`, `table:`.

---

## Image Guidelines
- PNG/JPEG supported for **PDF** and **DOCX**.
- SVG works for **PDF** only (DOCX not supported).
- Images auto-scale to page width (`max-width: 100%`) and center.
- Keep size reasonable (< 1 MB recommended).

---

## Examples (PowerShell)

**1) JSON text → PDF**
~~~powershell
Invoke-WebRequest -Method POST "http://127.0.0.1:8000/render" `
  -Form @{
    "json_text" = '{"title":"My Report","sections":[{"heading":"Intro","type":"paragraph","text":"Hello"}]}'
    "output"    = "pdf"
    "title"     = "Demo Report"
  } -OutFile demo.pdf
~~~

**2) JSON file + image → DOCX**
~~~powershell
Invoke-WebRequest -Method POST "http://127.0.0.1:8000/render" `
  -Form @{
    "text"   = Get-Item ".\text.json"
    "image"  = Get-Item ".\chart.png"
    "output" = "docx"
    "title"  = "Report With Image"
  } -OutFile demo.docx
~~~

---

## Notes
- For production containers, install `wkhtmltopdf` in the image to avoid host dependency issues.
- Validate input JSON before calling `/render`.

YOLO test.
