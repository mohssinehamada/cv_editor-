from typing import List, Optional

from pydantic import BaseModel

from app.schemas.common import GapReport, KeywordMap, Recommendation, ScoreBreakdown


class AnalyzeRequest(BaseModel):
    job_text: str
    resume_text: str
    provider: str
    model: Optional[str] = None


class AnalyzeResponse(BaseModel):
    scores: ScoreBreakdown
    gaps: GapReport
    recommendations: List[Recommendation]
    keyword_map: KeywordMap
    rewrites: Optional[dict] = None
