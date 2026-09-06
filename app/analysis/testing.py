import os

from app.analysis.base import Analyzer
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.models.repository_context import RepositoryContext


class TestingAnalyzer(Analyzer):

    def analyze(
        self,
        source_code: str,
        file_path: str,
    ) -> list[Finding]:

        return []

    def analyze_repository(
        self,
        context: RepositoryContext,
    ) -> list[Finding]:

        findings = []

        for changed_file in context.changed_files:

            if not changed_file.path.endswith(".py"):
                continue

            if changed_file.path.startswith("tests/"):
                continue

            file_name = os.path.basename(changed_file.path)
            file_name_without_extension = os.path.splitext(
                file_name
            )[0]

            expected_test_name = (
                f"test_{file_name_without_extension}.py"
            )

            has_matching_test = any(
                os.path.basename(path) == expected_test_name
                for path in context.file_paths
            )

            if has_matching_test:
                continue

            findings.append(
                Finding(
                    id=f"testing-missing-{changed_file.path}",
                    category=FindingCategory.TESTING,
                    severity=FindingSeverity.LOW,
                    confidence=0.75,
                    location=FindingLocation(
                        file_path=changed_file.path,
                        start_line=None,
                        end_line=None,
                    ),
                    title="Potential missing test coverage",
                    description=(
                        "No matching Python test file was found "
                        "for this changed source file."
                    ),
                    why_it_matters=(
                        "Changes without corresponding tests may "
                        "be harder to verify and can increase the "
                        "risk of regressions."
                    ),
                    recommendation=(
                        "Consider adding or updating tests for "
                        "the changed behavior."
                    ),
                    evidence=(
                        f"Expected test file: {expected_test_name}"
                    ),
                    source=FindingSource.TEST_ANALYZER,
                )
            )

        return findings