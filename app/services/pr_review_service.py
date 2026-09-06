from app.analysis.aggregator import FindingAggregator
from app.analysis.runner import AnalyzerRunner
from app.github.client import GitHubClient
from app.github.publisher import GitHubPublisher
from app.models.pull_request import ChangedFile
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.validator import FindingValidator


class PRReviewService:

    def __init__(
        self,
        github_client: GitHubClient,
        analyzer_runner: AnalyzerRunner,
        ai_review_engine: AIReviewEngine,
        aggregator: FindingAggregator,
        publisher: GitHubPublisher,
        validator: FindingValidator,
    ):
        self.github_client = github_client
        self.analyzer_runner = analyzer_runner
        self.ai_review_engine = ai_review_engine
        self.aggregator = aggregator
        self.publisher = publisher
        self.validator = validator

    def review_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> dict:

        # 1. Get Pull Request information
        pull_request = self.github_client.get_pull_request(
            owner,
            repo,
            pull_number,
        )

        head_commit = pull_request["head"]["sha"]

        # 2. Get changed files
        github_files = self.github_client.get_pull_request_files(
            owner,
            repo,
            pull_number,
        )

        changed_files = [
            ChangedFile(
                path=file["filename"],
                status=file["status"],
                additions=file["additions"],
                deletions=file["deletions"],
                patch=file.get("patch"),
            )
            for file in github_files
        ]

        all_findings = []
        warnings = []

        # 3. Analyze each changed file
        for changed_file in changed_files:

            # Currently we analyze Python files.
            if not changed_file.path.endswith(".py"):
                continue

            # 4. Get source code
            source_code = self.github_client.get_file_content(
                owner,
                repo,
                changed_file.path,
                head_commit,
            )

            # 5. Run static analyzers
            findings, analyzer_warnings = self.analyzer_runner.run(
                source_code,
                changed_file.path,
            )

            warnings.extend(analyzer_warnings)

            # 6. Validate static analyzer findings
            for finding in findings:

                is_valid, reason = self.validator.validate(
                    finding,
                    changed_file.path,
                )

                if is_valid:
                    all_findings.append(finding)
                else:
                    warnings.append(
                        f"Invalid finding rejected: "
                        f"{finding.id} - {reason}"
                    )

            # 7. Prepare AI review prompt
            ai_prompt = f"""
Review this changed Python file from a GitHub Pull Request.

File: {changed_file.path}

Code:

{source_code}

Focus on:

- Security
- Bugs
- Performance
- Code quality
- Testing

Only report meaningful issues.
Return findings using the required structured format.
"""

            # 8. Run AI review
            try:
                ai_result = self.ai_review_engine.review(
                    ai_prompt
                )

                # 9. Validate AI findings
                for finding in ai_result.findings:

                    is_valid, reason = self.validator.validate(
                        finding,
                        changed_file.path,
                    )

                    if is_valid:
                        all_findings.append(finding)
                    else:
                        warnings.append(
                            f"Invalid AI finding rejected: "
                            f"{finding.id} - {reason}"
                        )

            except Exception as error:
                warnings.append(
                    f"AI reviewer failed for "
                    f"{changed_file.path}: {error}"
                )

        # 10. Aggregate valid findings
        final_findings = self.aggregator.aggregate(
            all_findings
        )

        # 11. Publish review
        publish_result = self.publisher.publish_review(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            commit_id=head_commit,
            findings=final_findings,
        )

        # 12. Return complete result
        return {
            "pull_number": pull_number,
            "head_commit": head_commit,
            "changed_files": len(changed_files),
            "findings": final_findings,
            "warnings": warnings,
            "publish_result": publish_result,
        }