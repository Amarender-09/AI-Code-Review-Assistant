import ast

from app.analysis.base import Analyzer
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


class SecurityAnalyzer(Analyzer):

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

            if not isinstance(node, ast.Call):
                continue

            if not isinstance(node.func, ast.Name):
                continue

            if node.func.id != "eval":
                continue

            findings.append(
                Finding(
                    id=f"security-eval-{node.lineno}",
                    category=FindingCategory.SECURITY,
                    severity=FindingSeverity.HIGH,
                    confidence=0.95,
                    location=FindingLocation(
                        file_path=file_path,
                        start_line=node.lineno,
                        end_line=node.end_lineno,
                    ),
                    title="Use of eval()",
                    description=(
                        "The code uses eval(), which can execute "
                        "arbitrary Python expressions."
                    ),
                    why_it_matters=(
                        "If untrusted input reaches eval(), "
                        "an attacker may execute unintended code."
                    ),
                    recommendation=(
                        "Avoid eval() and use a safer alternative "
                        "that explicitly controls the allowed input."
                    ),
                    evidence="eval(...) call detected",
                    source=FindingSource.STATIC_ANALYZER,
                )
            )

        return findings