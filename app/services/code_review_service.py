from app.analysis.aggregator import FindingAggregator
from app.analysis.runner import AnalyzerRunner
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.validator import FindingValidator


class CodeReviewService:

    def __init__(
        self,
        analyzer_runner: AnalyzerRunner,
        ai_review_engine: AIReviewEngine,
        aggregator: FindingAggregator,
        validator: FindingValidator,
    ):
        self.analyzer_runner = analyzer_runner
        self.ai_review_engine = ai_review_engine
        self.aggregator = aggregator
        self.validator = validator

    def review_code(
        self,
        source_code: str,
        language: str,
    ) -> dict:

        file_path = self._get_file_path(language)

        all_findings = []
        warnings = []

        # 1. Run static analyzers
        static_findings, analyzer_warnings = (
            self.analyzer_runner.run(
                source_code,
                file_path,
            )
        )

        warnings.extend(analyzer_warnings)

        # 2. Validate static analyzer findings
        for finding in static_findings:

            is_valid, reason = self.validator.validate(
                finding,
                file_path,
            )

            if not is_valid:
                warnings.append(
                    f"Invalid finding rejected: "
                    f"{finding.id} - {reason}"
                )
                continue

            all_findings.append(finding)

        # 3. Prepare AI review prompt
        ai_prompt = f"""
Review the following {language} source code.

File: {file_path}

Code:

{source_code}

Focus on:

- Security
- Bugs
- Performance
- Code quality
- Testing

Only report meaningful issues in the provided code.

Do not report unrelated issues.

For every finding:

- Identify the exact location when possible.
- Explain the problem clearly.
- Explain why it matters.
- Provide a practical recommendation.
- Provide evidence from the code when possible.
- Assign an appropriate severity.
- Provide a confidence score.

Return findings using the required structured format.
"""

        # 4. Run AI review
        try:
            ai_result = self.ai_review_engine.review(
                ai_prompt
            )

            # 5. Validate AI findings
            for finding in ai_result.findings:

                is_valid, reason = self.validator.validate(
                    finding,
                    file_path,
                )

                if not is_valid:
                    warnings.append(
                        f"Invalid AI finding rejected: "
                        f"{finding.id} - {reason}"
                    )
                    continue

                all_findings.append(finding)

        except Exception as error:
            warnings.append(
                f"AI reviewer failed: {error}"
            )

        # 6. Aggregate findings
        final_findings = self.aggregator.aggregate(
            all_findings
        )

        # 7. Return review result
        return {
            "language": language,
            "file_path": file_path,
            "code_length": len(source_code),
            "findings": [
                finding.model_dump(mode="json")
                for finding in final_findings
            ],
            "warnings": warnings,
        }

    @staticmethod
    def _get_file_path(language: str) -> str:

        extensions = {
            "python": "pasted_code.py",
            "javascript": "pasted_code.js",
            "typescript": "pasted_code.ts",
        }

        return extensions.get(
            language.lower(),
            "pasted_code.txt",
        )