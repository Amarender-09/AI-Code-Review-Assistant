from app.models.finding import Finding


class FindingValidator:

    def validate(
        self,
        finding: Finding,
        expected_file_path: str,
    ) -> tuple[bool, str | None]:

        # 1. Validate title
        if not finding.title.strip():
            return False, "Finding title is empty"

        # 2. Validate description
        if not finding.description.strip():
            return False, "Finding description is empty"

        # 3. Validate confidence
        if not 0 <= finding.confidence <= 1:
            return False, "Finding confidence must be between 0 and 1"

        # 4. Validate file location
        if finding.location.file_path != expected_file_path:
            return (
                False,
                f"Finding points to {finding.location.file_path}, "
                f"but expected {expected_file_path}",
            )

        # 5. Validate start line
        if finding.location.start_line is not None:
            if finding.location.start_line < 1:
                return False, "Finding start line must be at least 1"

        # 6. Validate end line
        if finding.location.end_line is not None:
            if finding.location.end_line < 1:
                return False, "Finding end line must be at least 1"

        # 7. Validate line order
        start_line = finding.location.start_line
        end_line = finding.location.end_line

        if (
            start_line is not None
            and end_line is not None
            and end_line < start_line
        ):
            return False, "Finding end line cannot be before start line"

        return True, None