import json, os
from typing import Dict, Any, Optional
from fastapi import HTTPException
from starlette.responses import Response

from renderers.html_renderer import json_to_html
from renderers.pdf_renderer import html_to_pdf_bytes
from renderers.docx_renderer import render_docx_bytes

def parse_json(json_text: str) -> Dict[str, Any]:
    try:
        data = json.loads(json_text)
        if not isinstance(data, dict):
            raise ValueError("JSON_ROOT_NOT_OBJECT")
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": "INVALID_JSON", "detail": str(e)})

def build_html(data: Dict[str, Any], title: str, img_b64: Optional[str]) -> str:
    return json_to_html(data, title=title, img_b64=img_b64)

def render_pdf_response(html: str, title: str) -> Response:
    pdf_bytes = html_to_pdf_bytes(html)
    return Response(
        pdf_bytes,
        200,
        headers={"Content-Disposition": f'attachment; filename="{title}.pdf"'},
        media_type="application/pdf",
    )

def render_docx_response(data: Dict[str, Any], title: str, img_path: Optional[str]) -> Response:
    docx_bytes = render_docx_bytes(data, title=title, img_path=img_path)
    return Response(
        docx_bytes,
        200,
        headers={"Content-Disposition": f'attachment; filename="{title}.docx"'},
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
