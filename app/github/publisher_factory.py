from app.core import config
from app.github.client import GitHubClient
from app.github.fake_publisher import FakeGitHubPublisher
from app.github.publisher import GitHubPublisher, ReviewCommentBuilder
from app.github.real_publisher import RealGitHubPublisher
from app.reviewers.formatter import ReviewFormatter


def create_github_publisher() -> GitHubPublisher:

    if config.DRY_RUN:
        return FakeGitHubPublisher()

    github_client = GitHubClient()
    formatter = ReviewFormatter()
    comment_builder = ReviewCommentBuilder(formatter)

    return RealGitHubPublisher(
        github_client=github_client,
        comment_builder=comment_builder,
    )