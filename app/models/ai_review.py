from pydantic import BaseModel

from app.models.finding import Finding


class AIReviewResult(BaseModel):
    findings: list[Finding]