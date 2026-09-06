from app.reviewers.ai_provider import AIProvider


class FakeAIProvider(AIProvider):

    def generate_review(
        self,
        prompt: str,
    ) -> str:

        return """
{
    "findings": [
        {
            "id": "ai-001",
            "category": "security",
            "severity": "high",
            "confidence": 0.95,
            "location": {
                "file_path": "auth/login.py",
                "start_line": 2,
                "end_line": 2
            },
            "title": "Unsafe eval usage",
            "description": "User input is passed to eval.",
            "why_it_matters": "This may allow arbitrary code execution.",
            "recommendation": "Avoid eval with untrusted input.",
            "evidence": "eval(user_input)",
            "source": "ai_reviewer"
        }
    ]
}
"""