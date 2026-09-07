from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.reviewers.validator import FindingValidator


def create_finding(
    file_path="example.py",
    start_line=5,
    end_line=5,
    confidence=0.9,
):
    return Finding(
        id="test-finding",
        category=FindingCategory.BUG,
        severity=FindingSeverity.MEDIUM,
        confidence=confidence,
        location=FindingLocation(
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
        ),
        title="Test finding",
        description="Test description",
        why_it_matters="Test impact",
        recommendation="Test recommendation",
        evidence=None,
        source=FindingSource.STATIC_ANALYZER,
    )


def test_validator_accepts_valid_finding():
    validator = FindingValidator()

    finding = create_finding()

    is_valid, reason = validator.validate(
        finding,
        "example.py",
    )

    assert is_valid is True
    assert reason is None


def test_validator_rejects_wrong_file():
    validator = FindingValidator()

    finding = create_finding(
        file_path="other.py",
    )

    is_valid, reason = validator.validate(
        finding,
        "example.py",
    )

    assert is_valid is False
    assert "expected example.py" in reason


def test_validator_rejects_invalid_confidence():
    validator = FindingValidator()

    finding = create_finding(
        confidence=1.5,
    )

    is_valid, reason = validator.validate(
        finding,
        "example.py",
    )

    assert is_valid is False
    assert "confidence must be between 0 and 1" in reason


def test_validator_rejects_invalid_line_range():
    validator = FindingValidator()

    finding = create_finding(
        start_line=10,
        end_line=5,
    )

    is_valid, reason = validator.validate(
        finding,
        "example.py",
    )

    assert is_valid is False
    assert "end line cannot be before start line" in reason