import base64, os, tempfile
from typing import Optional, Tuple
from fastapi import UploadFile

def save_temp_upload(image: Optional[UploadFile]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if not image:
        return None, None, None
    b = image.file.read()
    _, ext = os.path.splitext(image.filename or "")
    ext = (ext or ".png").lower()
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tf.write(b); tf.close()
    b64 = base64.b64encode(b).decode("ascii")
    return tf.name, ext, b64
