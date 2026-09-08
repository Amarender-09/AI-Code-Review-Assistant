import re

from app.analysis.aggregator import FindingAggregator
from app.analysis.runner import AnalyzerRunner
from app.github.client import GitHubClient
from app.github.context_builder import build_code_context
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

            # 5. Build focused code context
            code_context = build_code_context(
                changed_file,
                source_code,
            )

            # 6. Get changed line numbers from the PR diff
            changed_lines = self._get_changed_line_numbers(
                changed_file.patch
            )

            # 7. Run static analyzers
            findings, analyzer_warnings = self.analyzer_runner.run(
                source_code,
                changed_file.path,
            )

            warnings.extend(analyzer_warnings)

            # 8. Validate static analyzer findings
            for finding in findings:

                is_valid, reason = self.validator.validate(
                    finding,
                    changed_file.path,
                )

                if not is_valid:
                    warnings.append(
                        f"Invalid finding rejected: "
                        f"{finding.id} - {reason}"
                    )
                    continue

                if not self._is_publishable_location(
                    finding,
                    changed_lines,
                ):
                    warnings.append(
                        f"Finding not on a changed line: "
                        f"{finding.id} - "
                        f"{changed_file.path}:"
                        f"{finding.location.start_line}"
                    )
                    continue

                all_findings.append(finding)

            # 9. Prepare focused AI review prompt
            ai_prompt = f"""
Review this changed Python file from a GitHub Pull Request.

File: {code_context.file_path}

Language: {code_context.language}

Changed code:

{code_context.changed_code}

Surrounding code:

{code_context.surrounding_code}

Focus on:

- Security
- Bugs
- Performance
- Code quality
- Testing

Only report meaningful issues in the changed code.

Do not report issues that are unrelated to the changed code.

Return findings using the required structured format.
"""

            # 10. Run AI review
            try:
                ai_result = self.ai_review_engine.review(
                    ai_prompt
                )

                # 11. Validate AI findings
                for finding in ai_result.findings:

                    is_valid, reason = self.validator.validate(
                        finding,
                        changed_file.path,
                    )

                    if not is_valid:
                        warnings.append(
                            f"Invalid AI finding rejected: "
                            f"{finding.id} - {reason}"
                        )
                        continue

                    if not self._is_publishable_location(
                        finding,
                        changed_lines,
                    ):
                        warnings.append(
                            f"AI finding not on a changed line: "
                            f"{finding.id} - "
                            f"{changed_file.path}:"
                            f"{finding.location.start_line}"
                        )
                        continue

                    all_findings.append(finding)

            except Exception as error:
                warnings.append(
                    f"AI reviewer failed for "
                    f"{changed_file.path}: {error}"
                )

        # 12. Aggregate valid findings
        final_findings = self.aggregator.aggregate(
            all_findings
        )

        # 13. Publish review
        publish_result = self.publisher.publish_review(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            commit_id=head_commit,
            findings=final_findings,
        )

        # 14. Return complete result
        return {
            "pull_number": pull_number,
            "head_commit": head_commit,
            "changed_files": len(changed_files),
            "findings": final_findings,
            "warnings": warnings,
            "publish_result": publish_result,
        }

    @staticmethod
    def _get_changed_line_numbers(
        patch: str | None,
    ) -> set[int]:
        """
        Return the new-file line numbers that were added
        or changed in the GitHub PR diff.
        """

        if not patch:
            return set()

        changed_lines = set()
        current_line = None

        for line in patch.splitlines():

            # Example:
            # @@ -1,5 +1,7 @@
            match = re.match(
                r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@",
                line,
            )

            if match:
                current_line = int(match.group(1))
                continue

            if current_line is None:
                continue

            if line.startswith("+") and not line.startswith("+++"):
                changed_lines.add(current_line)
                current_line += 1

            elif line.startswith("-") and not line.startswith("---"):
                # Deleted lines do not exist in the new file.
                continue

            else:
                current_line += 1

        return changed_lines

    @staticmethod
    def _is_publishable_location(
        finding,
        changed_lines: set[int],
    ) -> bool:

        line = finding.location.start_line

        if line is None:
            return False

        return line in changed_lines