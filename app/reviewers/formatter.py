from app.models.finding import Finding


class ReviewFormatter:
    def format_finding(self, finding: Finding) -> str:
        severity = finding.severity.value.upper()

        lines = [
            f"### {severity} — {finding.title}",
            "",
            f"**Category:** `{finding.category.value}`",
            f"**Confidence:** `{finding.confidence:.0%}`",
            "",
            "**Problem**",
            finding.description,
            "",
            "**Why it matters**",
            finding.why_it_matters,
            "",
            "**Recommendation**",
            finding.recommendation,
        ]

        if finding.evidence:
            lines.extend(
                [
                    "",
                    "**Evidence**",
                    f"```text",
                    finding.evidence,
                    "```",
                ]
            )

        return "\n".join(lines)

    def format_review(self, findings: list[Finding]) -> str:
        if not findings:
            return "## AI Code Review\n\nNo issues found."

        sections = [
            "## AI Code Review",
            "",
            f"Found **{len(findings)}** issue(s).",
            "",
        ]

        for finding in findings:
            sections.append(self.format_finding(finding))
            sections.append("\n---\n")

        return "\n".join(sections)