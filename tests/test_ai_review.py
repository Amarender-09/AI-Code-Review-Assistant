from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.fake_provider import FakeAIProvider


def test_ai_review_engine_returns_findings():
    provider = FakeAIProvider()
    engine = AIReviewEngine(provider)

    result = engine.review(
        "Review this Python code for security problems."
    )

    assert result.findings
    assert len(result.findings) > 0

    finding = result.findings[0]

    assert finding.title
    assert finding.description
    assert finding.category
    assert finding.severity
    assert 0 <= finding.confidence <= 1