from app.reviewers.fake_provider import FakeAIProvider


def test_fake_ai_provider_returns_response():
    provider = FakeAIProvider()

    response = provider.generate_review(
        "Review this Python code for security problems."
    )

    assert response
    assert isinstance(response, str)