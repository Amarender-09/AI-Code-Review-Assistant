import ast

from app.analysis.base import Analyzer
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


class BugAnalyzer(Analyzer):

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

            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            statements = node.body

            for index, statement in enumerate(statements):

                if not isinstance(statement, ast.Return):
                    continue

                unreachable_statements = statements[index + 1:]

                for unreachable in unreachable_statements:
                    findings.append(
                        Finding(
                            id=f"bug-unreachable-{unreachable.lineno}",
                            category=FindingCategory.BUG,
                            severity=FindingSeverity.MEDIUM,
                            confidence=0.98,
                            location=FindingLocation(
                                file_path=file_path,
                                start_line=unreachable.lineno,
                                end_line=unreachable.end_lineno,
                            ),
                            title="Unreachable code",
                            description=(
                                "This code appears after a return statement "
                                "and cannot be executed."
                            ),
                            why_it_matters=(
                                "Unreachable code can indicate a logic "
                                "mistake and makes the code harder to maintain."
                            ),
                            recommendation=(
                                "Remove the unreachable code or move it "
                                "before the return statement if it is required."
                            ),
                            evidence="Statement appears after return",
                            source=FindingSource.STATIC_ANALYZER,
                        )
                    )

        return findings