import re


def get_changed_line_ranges(patch: str) -> list[tuple[int, int]]:
    """
    Extract changed line ranges from a unified diff patch.

    Returns:
        A list of (start_line, line_count) tuples.
    """

    ranges = []

    for line in patch.splitlines():
        match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)

        if not match:
            continue

        start_line = int(match.group(1))
        line_count = int(match.group(2) or 1)

        ranges.append((start_line, line_count))

    return ranges


def extract_surrounding_code(
    source_code: str,
    changed_ranges: list[tuple[int, int]],
    context_lines: int = 5,
) -> str:
    """
    Extract source code surrounding the changed lines.
    """

    source_lines = source_code.splitlines()

    if not source_lines or not changed_ranges:
        return ""

    first_changed_line = min(
        start
        for start, _ in changed_ranges
    )

    last_changed_line = max(
        start + count - 1
        for start, count in changed_ranges
    )

    start_index = max(
        first_changed_line - context_lines - 1,
        0,
    )

    end_index = min(
        last_changed_line + context_lines,
        len(source_lines),
    )

    selected_lines = source_lines[start_index:end_index]

    return "\n".join(selected_lines)