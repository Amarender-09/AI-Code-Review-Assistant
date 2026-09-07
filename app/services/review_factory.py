from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer
from app.github.client import GitHubClient
from app.github.publisher_factory import create_github_publisher
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.openai_provider import OpenAIProvider
from app.reviewers.validator import FindingValidator
from app.services.pr_review_service import PRReviewService


def create_pr_review_service() -> PRReviewService:
    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    analyzer_runner = AnalyzerRunner(analyzers)

    ai_provider = OpenAIProvider()
    ai_review_engine = AIReviewEngine(ai_provider)

    aggregator = FindingAggregator()
    validator = FindingValidator()

    github_client = GitHubClient()
    publisher = create_github_publisher()

    return PRReviewService(
        github_client=github_client,
        analyzer_runner=analyzer_runner,
        ai_review_engine=ai_review_engine,
        aggregator=aggregator,
        publisher=publisher,
        validator=validator,
    )