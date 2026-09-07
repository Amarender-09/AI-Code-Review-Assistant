from app.github.publisher import ReviewCommentBuilder
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.reviewers.formatter import ReviewFormatter


def test_review_comment_builder_creates_github_comment():
    finding = Finding(
        id="SEC-001",
        category=FindingCategory.SECURITY,
        severity=FindingSeverity.HIGH,
        confidence=0.95,
        location=FindingLocation(
            file_path="login.py",
            start_line=2,
            end_line=2,
        ),
        title="SQL injection vulnerability",
        description="User input is directly concatenated into a SQL query.",
        why_it_matters="An attacker could manipulate the query.",
        recommendation="Use a parameterized SQL query.",
        evidence="username is directly inserted into the query.",
        source=FindingSource.AI_REVIEWER,
    )

    builder = ReviewCommentBuilder(ReviewFormatter())

    comment = builder.build_comment(finding)

    assert comment is not None
    assert comment.path == "login.py"
    assert comment.line == 2
    assert comment.side == "RIGHT"

    assert "SQL injection vulnerability" in comment.body
    assert "security" in comment.body
    assert "95%" in comment.body
    assert "Use a parameterized SQL query." in comment.body


def test_review_comment_builder_skips_finding_without_line():
    finding = Finding(
        id="SEC-002",
        category=FindingCategory.SECURITY,
        severity=FindingSeverity.HIGH,
        confidence=0.95,
        location=FindingLocation(
            file_path="login.py",
            start_line=None,
            end_line=None,
        ),
        title="File-level security issue",
        description="A security issue exists in the file.",
        why_it_matters="The issue may expose the application.",
        recommendation="Fix the security issue.",
        evidence=None,
        source=FindingSource.AI_REVIEWER,
    )

    builder = ReviewCommentBuilder(ReviewFormatter())

    comment = builder.build_comment(finding)

    assert comment is None