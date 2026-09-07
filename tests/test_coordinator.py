from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.coordinator import ReviewCoordinator
from app.reviewers.fake_provider import FakeAIProvider


def test_review_coordinator_combines_analyzer_and_ai_findings():
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

    assert warnings == []

    # Static analyzers produce 3 findings.
    # Fake AI provider produces 1 additional finding.
    assert len(findings) == 4

    categories = {finding.category.value for finding in findings}

    assert "security" in categories
    assert "bug" in categories
    assert "performance" in categories

    assert any(
        finding.source.value == "ai_reviewer"
        for finding in findings
    )