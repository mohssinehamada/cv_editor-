from typing import Optional

from pydantic import BaseModel


class ParseRequest(BaseModel):
    text: Optional[str] = None
    file_name: Optional[str] = None
    file_bytes_base64: Optional[str] = None


class ParseResponse(BaseModel):
    normalized_text: str
    detected_format: str
