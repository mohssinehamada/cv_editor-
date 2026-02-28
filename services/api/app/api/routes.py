from fastapi import APIRouter, Header, HTTPException

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.health import HealthResponse
from app.schemas.parse import ParseRequest, ParseResponse
from app.schemas.rewrite import RewriteRequest, RewriteResponse
from app.services.parsing import parse_input

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/parse", response_model=ParseResponse)
def parse_document(payload: ParseRequest) -> ParseResponse:
    if not payload.text and not payload.file_bytes_base64:
        raise HTTPException(status_code=400, detail="text or file_bytes_base64 is required")

    try:
        normalized_text, detected_format = parse_input(
            text=payload.text,
            file_name=payload.file_name,
            file_bytes_base64=payload.file_bytes_base64,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ParseResponse(normalized_text=normalized_text, detected_format=detected_format)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_match(
    payload: AnalyzeRequest, x_llm_api_key: str | None = Header(default=None)
) -> AnalyzeResponse:
    if not x_llm_api_key:
        raise HTTPException(status_code=401, detail="x-llm-api-key header required")
    # Placeholder: real analysis to be implemented.
    return AnalyzeResponse(
        scores={
            "overall": 0.0,
            "skills": 0.0,
            "keywords": 0.0,
            "responsibilities": 0.0,
            "seniority": 0.0,
            "ats": 0.0,
        },
        gaps={"missing_skills": [], "weak_areas": [], "missing_sections": []},
        recommendations=[],
        keyword_map={"present_strong": [], "present_weak": [], "missing": []},
        rewrites=None,
    )


@router.post("/rewrite", response_model=RewriteResponse)
def rewrite_resume(
    payload: RewriteRequest, x_llm_api_key: str | None = Header(default=None)
) -> RewriteResponse:
    if not x_llm_api_key:
        raise HTTPException(status_code=401, detail="x-llm-api-key header required")
    # Placeholder: real rewrite to be implemented.
    return RewriteResponse(revised_markdown="", revised_structured={})

# POST /api/export/docx (optional)
