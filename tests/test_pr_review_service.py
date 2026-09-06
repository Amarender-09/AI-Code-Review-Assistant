from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer

from app.github.client import GitHubClient
from app.github.publisher import ReviewCommentBuilder

from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.formatter import ReviewFormatter
from app.reviewers.openai_provider import OpenAIProvider
from app.reviewers.validator import FindingValidator

from app.github.publisher_factory import create_github_publisher
from app.services.pr_review_service import PRReviewService


def main():
    # Static analyzers
    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    analyzer_runner = AnalyzerRunner(analyzers)

    # Real AI provider
    ai_provider = OpenAIProvider()
    ai_review_engine = AIReviewEngine(ai_provider)

    # Finding aggregation
    aggregator = FindingAggregator()

    # Finding validation
    validator = FindingValidator()

    # GitHub client for read operations
    github_client = GitHubClient()

    # Publisher is selected automatically
    # based on DRY_RUN configuration.
    publisher = create_github_publisher()

    # Complete PR review service
    service = PRReviewService(
        github_client=github_client,
        analyzer_runner=analyzer_runner,
        ai_review_engine=ai_review_engine,
        aggregator=aggregator,
        publisher=publisher,
        validator=validator,
    )

    # Test Pull Request
    result = service.review_pull_request(
        owner="Amarender-09",
        repo="AI-Code-Review-Test",
        pull_number=1,
    )

    # Results
    print("PR number:", result["pull_number"])
    print("Changed files:", result["changed_files"])
    print("Final findings:", len(result["findings"]))
    print("Warnings:", len(result["warnings"]))

    print("\nWarnings:")

    for warning in result["warnings"]:
        print("-", warning)

    print("\nPublish result:")
    print(result["publish_result"])

    print("\nFindings:")

    for finding in result["findings"]:
        print(
            f"- {finding.severity.value} | "
            f"{finding.category.value} | "
            f"{finding.title}"
        )


if __name__ == "__main__":
    main()