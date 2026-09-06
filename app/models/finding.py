from enum import Enum

from pydantic import BaseModel


class FindingCategory(str, Enum):
    SECURITY = "security"
    BUG = "bug"
    PERFORMANCE = "performance"
    CODE_QUALITY = "code_quality"
    TESTING = "testing"


class FindingSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingSource(str, Enum):
    STATIC_ANALYZER = "static_analyzer"
    AI_REVIEWER = "ai_reviewer"
    TEST_ANALYZER = "test_analyzer"


class FindingLocation(BaseModel):
    file_path: str
    start_line: int | None = None
    end_line: int | None = None


class Finding(BaseModel):
    id: str
    category: FindingCategory
    severity: FindingSeverity
    confidence: float

    location: FindingLocation

    title: str
    description: str
    why_it_matters: str
    recommendation: str

    evidence: str | None = None
    source: FindingSource