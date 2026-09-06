from app.github.publisher import GitHubPublisher
from app.models.finding import Finding


class FakeGitHubPublisher(GitHubPublisher):
    def publish_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        commit_id: str,
        findings: list[Finding],
    ) -> dict:

        return {
            "published": False,
            "mode": "dry_run",
            "owner": owner,
            "repo": repo,
            "pull_number": pull_number,
            "commit_id": commit_id,
            "finding_count": len(findings),
        }