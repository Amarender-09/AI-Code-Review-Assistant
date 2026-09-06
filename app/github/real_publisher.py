from app.github.client import GitHubClient
from app.github.publisher import GitHubPublisher, ReviewCommentBuilder
from app.models.finding import Finding


class RealGitHubPublisher(GitHubPublisher):
    def __init__(
        self,
        github_client: GitHubClient,
        comment_builder: ReviewCommentBuilder,
    ):
        self.github_client = github_client
        self.comment_builder = comment_builder

    def publish_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        commit_id: str,
        findings: list[Finding],
    ) -> dict:

        comments = self.comment_builder.build_comments(findings)

        if not comments:
            return {
                "published": False,
                "reason": "No publishable findings",
            }

        github_comments = [
            comment.model_dump()
            for comment in comments
        ]

        return self.github_client.create_pull_request_review(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            commit_id=commit_id,
            comments=github_comments,
        )