import ast

from app.analysis.base import Analyzer
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


class PerformanceAnalyzer(Analyzer):

    def analyze(
        self,
        source_code: str,
        file_path: str,
    ) -> list[Finding]:

        findings = []

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return findings

        for node in ast.walk(tree):

            if not isinstance(node, ast.For):
                continue

            for statement in node.body:

                if not isinstance(statement, ast.Assign):
                    continue

                if not isinstance(statement.value, ast.BinOp):
                    continue

                if not isinstance(statement.value.op, ast.Add):
                    continue

                if not isinstance(statement.value.left, ast.Name):
                    continue

                if not isinstance(statement.value.right, ast.List):
                    continue

                findings.append(
                    Finding(
                        id=f"performance-list-concat-{statement.lineno}",
                        category=FindingCategory.PERFORMANCE,
                        severity=FindingSeverity.MEDIUM,
                        confidence=0.90,
                        location=FindingLocation(
                            file_path=file_path,
                            start_line=statement.lineno,
                            end_line=statement.end_lineno,
                        ),
                        title="Repeated list concatenation in loop",
                        description=(
                            "A list is being created through concatenation "
                            "inside a loop."
                        ),
                        why_it_matters=(
                            "Repeated list concatenation can create new list "
                            "objects repeatedly and become inefficient for "
                            "larger collections."
                        ),
                        recommendation=(
                            "Consider using list.append() when adding "
                            "individual items to an existing list."
                        ),
                        evidence="List concatenation detected inside a for loop",
                        source=FindingSource.STATIC_ANALYZER,
                    )
                )

        return findings