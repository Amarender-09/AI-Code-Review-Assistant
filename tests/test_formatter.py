from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.reviewers.formatter import ReviewFormatter


def test_formatter_creates_review_with_finding_details():
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
        why_it_matters="An attacker could manipulate the query and access unauthorized data.",
        recommendation="Use a parameterized SQL query.",
        evidence="query = unsafe_query",
        source=FindingSource.AI_REVIEWER,
    )

    formatter = ReviewFormatter()

    result = formatter.format_review([finding])

    assert "## AI Code Review" in result
    assert "Found **1** issue(s)." in result
    assert "### HIGH — SQL injection vulnerability" in result
    assert "**Category:** `security`" in result
    assert "**Confidence:** `95%`" in result
    assert "**Problem**" in result
    assert finding.description in result
    assert "**Why it matters**" in result
    assert finding.why_it_matters in result
    assert "**Recommendation**" in result
    assert finding.recommendation in result
    assert "**Evidence**" in result
    assert finding.evidence in result


def test_formatter_handles_no_findings():
    formatter = ReviewFormatter()

    result = formatter.format_review([])

    assert result == "## AI Code Review\n\nNo issues found."