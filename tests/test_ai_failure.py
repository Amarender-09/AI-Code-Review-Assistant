from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.ai_provider import AIProvider


class InvalidJSONProvider(AIProvider):

    def generate_review(self, prompt: str) -> str:
        return "This is not valid JSON"


class InvalidFindingProvider(AIProvider):

    def generate_review(self, prompt: str) -> str:
        return """
{
    "findings": [
        {
            "id": "ai-002",
            "category": "security",
            "severity": "SUPER_IMPORTANT",
            "confidence": 0.95,
            "location": {
                "file_path": "auth/login.py",
                "start_line": 2,
                "end_line": 2
            },
            "title": "Test finding",
            "description": "Test description",
            "why_it_matters": "Test impact",
            "recommendation": "Test recommendation",
            "evidence": "Test evidence",
            "source": "ai_reviewer"
        }
    ]
}
"""


def test_invalid_json_response():
    engine = AIReviewEngine(InvalidJSONProvider())

    try:
        engine.review("Review this code.")
        assert False, "Expected ValueError for invalid JSON"
    except ValueError as error:
        assert "invalid JSON" in str(error)


def test_invalid_finding_response():
    engine = AIReviewEngine(InvalidFindingProvider())

    try:
        engine.review("Review this code.")
        assert False, "Expected ValueError for invalid finding"
    except ValueError as error:
        assert "validation" in str(error)