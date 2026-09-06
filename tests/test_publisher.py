from app.github.fake_publisher import FakeGitHubPublisher


publisher = FakeGitHubPublisher()

result = publisher.publish_review(
    owner="test-owner",
    repo="test-repo",
    pull_number=1,
    commit_id="abc123",
    findings=[],
)

print(result)