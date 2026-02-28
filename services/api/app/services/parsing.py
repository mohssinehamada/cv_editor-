from __future__ import annotations

import base64
import io
from typing import Optional, Tuple

from pypdf import PdfReader
from pypdf.errors import PdfReadError
import docx


def _normalize_text(text: str) -> str:
    # Simple normalization placeholder
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.strip() for line in text.split("\n")).strip()


def _detect_format(file_name: Optional[str], has_text: bool) -> str:
    if has_text:
        return "text"
    if not file_name:
        return "binary"
    lowered = file_name.lower()
    if lowered.endswith(".pdf"):
        return "pdf"
    if lowered.endswith(".docx"):
        return "docx"
    return "binary"


def _decode_base64(data: str) -> bytes:
    return base64.b64decode(data)


def parse_text(text: str) -> Tuple[str, str]:
    return _normalize_text(text), "text"


def parse_pdf(file_bytes: bytes) -> Tuple[str, str]:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text:
                parts.append(page_text)
        return _normalize_text("\n".join(parts)), "pdf"
    except PdfReadError as exc:
        raise ValueError("Failed to parse PDF") from exc
    except Exception as exc:
        raise ValueError("Unexpected error while parsing PDF") from exc


def parse_docx(file_bytes: bytes) -> Tuple[str, str]:
    try:
        document = docx.Document(io.BytesIO(file_bytes))
        parts = [para.text for para in document.paragraphs if para.text]
        return _normalize_text("\n".join(parts)), "docx"
    except Exception as exc:
        raise ValueError("Failed to parse DOCX") from exc


def parse_input(
    *, text: Optional[str], file_name: Optional[str], file_bytes_base64: Optional[str]
) -> Tuple[str, str]:
    if text:
        return parse_text(text)

    if file_bytes_base64:
        file_bytes = _decode_base64(file_bytes_base64)
        detected = _detect_format(file_name, has_text=False)
        if detected == "pdf":
            return parse_pdf(file_bytes)
        if detected == "docx":
            return parse_docx(file_bytes)
        # Unknown binary
        return "", detected

    return "", _detect_format(file_name, has_text=False)
