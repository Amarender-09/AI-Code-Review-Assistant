from app.github.fake_publisher import FakeGitHubPublisher


def test_fake_github_publisher_returns_dry_run_result():
    publisher = FakeGitHubPublisher()

    result = publisher.publish_review(
        owner="test-owner",
        repo="test-repo",
        pull_number=1,
        commit_id="abc123",
        findings=[],
    )

    assert result["published"] is False
    assert result["mode"] == "dry_run"
    assert result["owner"] == "test-owner"
    assert result["repo"] == "test-repo"
    assert result["pull_number"] == 1
    assert result["commit_id"] == "abc123"
    assert result["finding_count"] == 0