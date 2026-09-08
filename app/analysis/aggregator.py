from app.models.finding import Finding


SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}


class FindingAggregator:

    def aggregate(
        self,
        findings: list[Finding],
    ) -> list[Finding]:

        unique_findings = {}

        # Remove exact duplicates by finding ID
        for finding in findings:
            if finding.id not in unique_findings:
                unique_findings[finding.id] = finding

        deduplicated = list(unique_findings.values())

        # Remove findings that represent the same underlying issue
        deduplicated = self._remove_similar_findings(
            deduplicated
        )

        # Sort by severity
        deduplicated.sort(
            key=lambda finding: SEVERITY_ORDER[
                finding.severity.value
            ]
        )

        return deduplicated

    def _remove_similar_findings(
        self,
        findings: list[Finding],
    ) -> list[Finding]:

        selected = []

        for finding in findings:

            duplicate_index = self._find_similar_finding(
                finding,
                selected,
            )

            if duplicate_index is None:
                selected.append(finding)
                continue

            existing = selected[duplicate_index]

            # Keep the stronger finding
            if self._is_stronger(finding, existing):
                selected[duplicate_index] = finding

        return selected

    def _find_similar_finding(
        self,
        finding: Finding,
        selected: list[Finding],
    ):

        for index, existing in enumerate(selected):

            # Findings in different files are not duplicates
            if (
                finding.location.file_path
                != existing.location.file_path
            ):
                continue

            # Findings far apart are not duplicates
            if not self._lines_are_close(
                finding,
                existing,
            ):
                continue

            if self._is_same_underlying_issue(
                finding,
                existing,
            ):
                return index

        return None

    def _is_same_underlying_issue(
        self,
        first: Finding,
        second: Finding,
    ) -> bool:

        first_text = self._finding_text(first)
        second_text = self._finding_text(second)

        similarity = self._text_similarity(
            first_text,
            second_text,
        )

        if similarity >= 0.5:
            return True

        if self._share_issue_concept(
            first_text,
            second_text,
        ):
            return True

        return False

    def _lines_are_close(
        self,
        first: Finding,
        second: Finding,
    ) -> bool:

        first_line = first.location.start_line
        second_line = second.location.start_line

        if first_line is None or second_line is None:
            return False

        return abs(first_line - second_line) <= 2

    def _finding_text(
        self,
        finding: Finding,
    ) -> set[str]:

        text = " ".join(
            [
                finding.title,
                finding.description,
                finding.why_it_matters,
            ]
        )

        return self._meaningful_words(text)

    def _text_similarity(
        self,
        first: set[str],
        second: set[str],
    ) -> float:

        if not first or not second:
            return 0.0

        return (
            len(first.intersection(second))
            / min(len(first), len(second))
        )

    def _share_issue_concept(
        self,
        first: set[str],
        second: set[str],
    ) -> bool:

        issue_concepts = [
            {"unreachable", "return"},
            {"eval"},
            {"sql", "injection"},
            {"password", "credential"},
            {"list", "concatenation"},
        ]

        for concept in issue_concepts:

            if concept.issubset(first) and concept.issubset(second):
                return True

        return False

    def _meaningful_words(
        self,
        text: str,
    ) -> set[str]:

        ignored_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "to",
            "in",
            "of",
            "and",
            "for",
            "causes",
            "code",
            "statement",
            "this",
            "that",
            "may",
            "be",
            "with",
            "after",
            "via",
        }

        words = {
            word.strip(".,:;()[]{}").lower()
            for word in text.split()
        }

        return {
            word
            for word in words
            if word and word not in ignored_words
        }

    def _is_stronger(
        self,
        first: Finding,
        second: Finding,
    ) -> bool:

        first_severity = SEVERITY_ORDER[
            first.severity.value
        ]

        second_severity = SEVERITY_ORDER[
            second.severity.value
        ]

        if first_severity != second_severity:
            return first_severity < second_severity

        return first.confidence > second.confidence