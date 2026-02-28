from typing import List, Optional

from pydantic import BaseModel


class ScoreBreakdown(BaseModel):
    overall: float
    skills: float
    keywords: float
    responsibilities: float
    seniority: float
    ats: float


class GapReport(BaseModel):
    missing_skills: List[str]
    weak_areas: List[str]
    missing_sections: List[str]


class Recommendation(BaseModel):
    priority: str  # P0/P1/P2
    action: str  # add/edit/remove/reorder
    section: str
    why: str
    how: str
    example_rewrite: Optional[str] = None
    risk_flag: bool


class KeywordMap(BaseModel):
    present_strong: List[str]
    present_weak: List[str]
    missing: List[str]
