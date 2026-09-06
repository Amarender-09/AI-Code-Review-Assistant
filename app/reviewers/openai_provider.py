from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL
from app.reviewers.ai_provider import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(
        self,
        api_key: str | None = OPENAI_API_KEY,
        model: str = OPENAI_MODEL,
    ):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_review(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ai_review_result",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "findings": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "category": {
                                            "type": "string",
                                            "enum": [
                                                "security",
                                                "bug",
                                                "performance",
                                                "code_quality",
                                                "testing",
                                            ],
                                        },
                                        "severity": {
                                            "type": "string",
                                            "enum": [
                                                "critical",
                                                "high",
                                                "medium",
                                                "low",
                                                "info",
                                            ],
                                        },
                                        "confidence": {
                                            "type": "number",
                                        },
                                        "location": {
                                            "type": "object",
                                            "properties": {
                                                "file_path": {"type": "string"},
                                                "start_line": {
                                                    "type": ["integer", "null"]
                                                },
                                                "end_line": {
                                                    "type": ["integer", "null"]
                                                },
                                            },
                                            "required": [
                                                "file_path",
                                                "start_line",
                                                "end_line",
                                            ],
                                            "additionalProperties": False,
                                        },
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "why_it_matters": {"type": "string"},
                                        "recommendation": {"type": "string"},
                                        "evidence": {
                                            "type": ["string", "null"]
                                        },
                                        "source": {
                                            "type": "string",
                                            "enum": [
                                                "ai_reviewer"
                                            ],
                                        },
                                    },
                                    "required": [
                                        "id",
                                        "category",
                                        "severity",
                                        "confidence",
                                        "location",
                                        "title",
                                        "description",
                                        "why_it_matters",
                                        "recommendation",
                                        "evidence",
                                        "source",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["findings"],
                        "additionalProperties": False,
                    },
                }
            },
        )

        return response.output_text