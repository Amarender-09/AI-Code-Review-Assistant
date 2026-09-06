from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.coordinator import ReviewCoordinator
from app.reviewers.fake_provider import FakeAIProvider


def main():

    source_code = """def process(user_input, items):
    result = eval(user_input)

    for item in items:
        result = result + [item]

    return result
    print("unreachable")
"""

    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    analyzer_runner = AnalyzerRunner(analyzers)

    ai_provider = FakeAIProvider()
    ai_review_engine = AIReviewEngine(ai_provider)

    aggregator = FindingAggregator()

    coordinator = ReviewCoordinator(
        analyzer_runner=analyzer_runner,
        ai_review_engine=ai_review_engine,
        aggregator=aggregator,
    )

    findings, warnings = coordinator.review(
        source_code=source_code,
        file_path="example.py",
        ai_prompt="Review this Python code.",
    )

    print("Final findings:", len(findings))

    for finding in findings:
        print(
            finding.severity.value,
            "|",
            finding.category.value,
            "|",
            finding.title,
        )

    print("\nWarnings:", len(warnings))

    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    main()