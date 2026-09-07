from app.analysis.testing import TestingAnalyzer
from app.models.pull_request import ChangedFile, Repository
from app.models.repository_context import RepositoryContext


def test_testing_analyzer_detects_missing_test():
    repository = Repository(
        owner="example",
        name="demo-project",
        full_name="example/demo-project",
        default_branch="main",
    )

    changed_files = [
        ChangedFile(
            path="auth/login.py",
            status="modified",
            additions=10,
            deletions=3,
            patch=None,
        ),
        ChangedFile(
            path="auth/payment.py",
            status="modified",
            additions=15,
            deletions=2,
            patch=None,
        ),
    ]

    context = RepositoryContext(
        repository=repository,
        changed_files=changed_files,
        file_paths=[
            "auth/login.py",
            "tests/test_login.py",
            "auth/payment.py",
        ],
    )

    analyzer = TestingAnalyzer()

    findings = analyzer.analyze_repository(context)

    assert len(findings) == 1

    finding = findings[0]

    assert finding.category.value == "testing"
    assert finding.severity.value == "low"
    assert finding.location.file_path == "auth/payment.py"
    assert finding.location.start_line is None
    assert "test" in finding.title.lower()