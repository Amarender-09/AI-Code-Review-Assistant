from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.fake_provider import FakeAIProvider


def main():

    provider = FakeAIProvider()

    engine = AIReviewEngine(provider)

    result = engine.review(
        "Review this Python code for security problems."
    )

    print("AI findings:", len(result.findings))

    for finding in result.findings:
        print(finding.model_dump())


if __name__ == "__main__":
    main()