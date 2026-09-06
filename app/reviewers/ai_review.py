import json

from pydantic import ValidationError

from app.models.ai_review import AIReviewResult
from app.reviewers.ai_provider import AIProvider


class AIReviewEngine:

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def review(self, prompt: str) -> AIReviewResult:

        response = self.provider.generate_review(prompt)

        return self.parse_response(response)

    def parse_response(
        self,
        response: str,
    ) -> AIReviewResult:

        try:
            data = json.loads(response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "AI provider returned invalid JSON"
            ) from error

        try:
            return AIReviewResult.model_validate(data)

        except ValidationError as error:
            raise ValueError(
                f"AI response failed validation: {error}"
            ) from error