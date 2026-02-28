from typing import Optional

from pydantic import BaseModel


class RewriteRequest(BaseModel):
    job_text: str
    resume_structured: dict
    target_role: Optional[str] = None


class RewriteResponse(BaseModel):
    revised_markdown: str
    revised_structured: dict
