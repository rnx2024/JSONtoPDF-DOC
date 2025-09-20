from typing import Optional, List, Any
from pydantic import BaseModel

class Section(BaseModel):
    heading: Optional[str] = None
    type: str  # "paragraph" | "table" | "list"
    text: Optional[str] = None
    rows: Optional[List[List[Any]]] = None
    items: Optional[List[Any]] = None

class StructuredDoc(BaseModel):
    title: Optional[str] = None
    sections: List[Section]
