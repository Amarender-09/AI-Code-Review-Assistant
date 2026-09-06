from abc import ABC, abstractmethod

from app.models.finding import Finding
from app.models.github_review import GitHubReviewComment
from app.reviewers.formatter import ReviewFormatter


class GitHubPublisher(ABC):
    @abstractmethod
    def publish_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        commit_id: str,
        findings: list[Finding],
    ) -> dict:
        pass


class ReviewCommentBuilder:
    def __init__(self, formatter: ReviewFormatter):
        self.formatter = formatter

    def build_comment(
        self,
        finding: Finding,
    ) -> GitHubReviewComment | None:

        line = finding.location.start_line

        if line is None:
            return None

        return GitHubReviewComment(
            path=finding.location.file_path,
            line=line,
            side="RIGHT",
            body=self.formatter.format_finding(finding),
        )

    def build_comments(
        self,
        findings: list[Finding],
    ) -> list[GitHubReviewComment]:

        comments = []

        for finding in findings:
            comment = self.build_comment(finding)

            if comment is not None:
                comments.append(comment)

        return comments