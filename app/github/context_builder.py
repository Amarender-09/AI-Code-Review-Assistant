from app.github.diff_parser import (
    extract_surrounding_code,
    get_changed_line_ranges,
)
from app.models.code_context import CodeContext
from app.models.pull_request import ChangedFile


def detect_language(file_path: str) -> str:
    extension = (
        file_path.rsplit(".", 1)[-1].lower()
        if "." in file_path
        else ""
    )

    language_map = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "cpp": "cpp",
        "c": "c",
        "cs": "csharp",
        "rb": "ruby",
        "php": "php",
    }

    return language_map.get(extension, "unknown")


def build_code_context(
    changed_file: ChangedFile,
    source_code: str,
) -> CodeContext:

    patch = changed_file.patch or ""

    changed_ranges = get_changed_line_ranges(patch)

    surrounding_code = extract_surrounding_code(
        source_code,
        changed_ranges,
        context_lines=5,
    )

    return CodeContext(
        file_path=changed_file.path,
        language=detect_language(changed_file.path),
        changed_code=patch,
        surrounding_code=surrounding_code,
        related_tests=[],
    )