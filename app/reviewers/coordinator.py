from app.analysis.aggregator import FindingAggregator
from app.analysis.runner import AnalyzerRunner
from app.models.finding import Finding
from app.reviewers.ai_review import AIReviewEngine


class ReviewCoordinator:

    def __init__(
        self,
        analyzer_runner: AnalyzerRunner,
        ai_review_engine: AIReviewEngine,
        aggregator: FindingAggregator,
    ):
        self.analyzer_runner = analyzer_runner
        self.ai_review_engine = ai_review_engine
        self.aggregator = aggregator

    def review(
        self,
        source_code: str,
        file_path: str,
        ai_prompt: str,
    ) -> tuple[list[Finding], list[str]]:

        findings, warnings = self.analyzer_runner.run(
            source_code,
            file_path,
        )

        try:
            ai_result = self.ai_review_engine.review(
                ai_prompt
            )

            findings.extend(ai_result.findings)

        except Exception as error:
            warnings.append(
                f"AI reviewer failed: {error}"
            )

        final_findings = self.aggregator.aggregate(
            findings
        )

        return final_findings, warnings