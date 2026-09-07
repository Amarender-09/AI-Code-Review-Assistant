from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


def test_finding_model():
    finding = Finding(
        id="finding-001",
        category=FindingCategory.SECURITY,
        severity=FindingSeverity.HIGH,
        confidence=0.95,
        location=FindingLocation(
            file_path="auth/login.py",
            start_line=42,
            end_line=42,
        ),
        title="Potential unsafe code execution",
        description="User-controlled input may be executed as code.",
        why_it_matters="An attacker may be able to execute unintended code.",
        recommendation="Avoid executing user-controlled input.",
        evidence="eval(user_input)",
        source=FindingSource.STATIC_ANALYZER,
    )

    assert finding.id == "finding-001"
    assert finding.category == FindingCategory.SECURITY
    assert finding.severity == FindingSeverity.HIGH
    assert finding.confidence == 0.95
    assert finding.location.file_path == "auth/login.py"
    assert finding.location.start_line == 42
    assert finding.location.end_line == 42
    assert finding.source == FindingSource.STATIC_ANALYZER