from app.github.publisher import ReviewCommentBuilder
from app.github.real_publisher import RealGitHubPublisher
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.reviewers.formatter import ReviewFormatter


class FakeGitHubClient:

    def __init__(self):
        self.calls = []

    def create_pull_request_review(
        self,
        owner,
        repo,
        pull_number,
        commit_id,
        comments,
    ):
        self.calls.append(
            {
                "owner": owner,
                "repo": repo,
                "pull_number": pull_number,
                "commit_id": commit_id,
                "comments": comments,
            }
        )

        return {
            "id": 123,
            "body": "Fake GitHub review",
        }


def main():

    # Fake GitHub client.
    # This means NO real GitHub request is made.
    github_client = FakeGitHubClient()

    formatter = ReviewFormatter()
    comment_builder = ReviewCommentBuilder(formatter)

    publisher = RealGitHubPublisher(
        github_client=github_client,
        comment_builder=comment_builder,
    )

    finding = Finding(
        id="test-security-001",
        category=FindingCategory.SECURITY,
        severity=FindingSeverity.HIGH,
        confidence=0.95,
        location=FindingLocation(
            file_path="app.py",
            start_line=12,
            end_line=12,
        ),
        title="Unsafe eval usage",
        description="User input is passed to eval.",
        why_it_matters="This may allow arbitrary code execution.",
        recommendation="Avoid eval with untrusted input.",
        evidence="eval(user_input)",
        source=FindingSource.AI_REVIEWER,
    )

    result = publisher.publish_review(
        owner="Amarender-09",
        repo="AI-Code-Review-Test",
        pull_number=1,
        commit_id="test-commit-123",
        findings=[finding],
    )

    print("Publisher result:")
    print(result)

    print("\nGitHub request:")
    print(github_client.calls[0])

    # Verify repository
    assert github_client.calls[0]["owner"] == "Amarender-09"
    assert github_client.calls[0]["repo"] == "AI-Code-Review-Test"

    # Verify PR
    assert github_client.calls[0]["pull_number"] == 1

    # Verify commit
    assert github_client.calls[0]["commit_id"] == "test-commit-123"

    # Verify comment
    comments = github_client.calls[0]["comments"]

    assert len(comments) == 1
    assert comments[0]["path"] == "app.py"
    assert comments[0]["line"] == 12
    assert comments[0]["side"] == "RIGHT"

    assert "Unsafe eval usage" in comments[0]["body"]

    print("\nReal publisher test passed.")


if __name__ == "__main__":
    main()