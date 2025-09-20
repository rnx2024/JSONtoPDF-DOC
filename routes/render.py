from fastapi import APIRouter, Form, File, UploadFile
from starlette.responses import Response
from typing import Optional
import os, json

from services.render_service import (
    parse_json,
    build_html,
    render_pdf_response,
    render_docx_response,
)
from utils.images import save_temp_upload

router = APIRouter()

@router.get("/health")
async def health() -> dict:
    return {"ok": True}

@router.post("/render")
async def render(
    # Accept EITHER JSON text OR JSON file
    json_text: Optional[str] = Form(None),
    text: Optional[UploadFile] = File(None),
    output: str = Form(...),
    title: str = Form("Document"),
    image: Optional[UploadFile] = File(None),
):
    # Parse JSON
    try:
        if text is not None:
            payload_bytes = await text.read()
            data = json.loads(payload_bytes.decode("utf-8"))
        elif json_text is not None:
            data = parse_json(json_text)
        else:
            return Response(
                '{"error":"MISSING_JSON"}',
                400,
                media_type="application/json",
            )
    except Exception as e:
        return Response(
            f'{{"error":"INVALID_JSON","detail":"{str(e)}"}}',
            400,
            media_type="application/json",
        )

    # Save image if provided
    img_path, img_ext, img_b64 = save_temp_upload(image)

    try:
        if output.lower() == "docx" and img_ext == ".svg":
            return Response(
                '{"error":"SVG_NOT_SUPPORTED_FOR_DOCX"}',
                400,
                media_type="application/json",
            )

        html = build_html(data, title=title, img_b64=img_b64)

        if output.lower() == "pdf":
            return render_pdf_response(html, title)
        elif output.lower() == "docx":
            return render_docx_response(data, title, img_path)
        else:
            return Response(
                '{"error":"INVALID_OUTPUT"}',
                400,
                media_type="application/json",
            )
    finally:
        if img_path and os.path.exists(img_path):
            try:
                os.unlink(img_path)
            except Exception:
                pass
