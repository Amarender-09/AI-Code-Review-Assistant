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


def test_provider(provider):
    engine = AIReviewEngine(provider)

    try:
        engine.review("Review this code.")
        print("ERROR: Invalid response was accepted")

    except ValueError as error:
        print("Controlled error:")
        print(error)


def main():
    print("=== Invalid JSON ===")
    test_provider(InvalidJSONProvider())

    print("\n=== Invalid Finding ===")
    test_provider(InvalidFindingProvider())


if __name__ == "__main__":
    main()