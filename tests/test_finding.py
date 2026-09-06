from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


def main():
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

    print("Finding:")
    print(finding.model_dump())


if __name__ == "__main__":
    main()