from app.analysis.aggregator import FindingAggregator
from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)


def create_finding(
    finding_id: str,
    severity: FindingSeverity,
    category: FindingCategory,
    file_path: str,
    line: int,
    confidence: float,
    source: FindingSource,
) -> Finding:

    return Finding(
        id=finding_id,
        category=category,
        severity=severity,
        confidence=confidence,
        location=FindingLocation(
            file_path=file_path,
            start_line=line,
            end_line=line,
        ),
        title=f"Finding {finding_id}",
        description="Test finding",
        why_it_matters="Test impact",
        recommendation="Test recommendation",
        evidence=None,
        source=source,
    )


def main():

    findings = [

        # Exact duplicate ID
        create_finding(
            "duplicate-1",
            FindingSeverity.LOW,
            FindingCategory.BUG,
            "example.py",
            10,
            0.80,
            FindingSource.STATIC_ANALYZER,
        ),

        create_finding(
            "duplicate-1",
            FindingSeverity.LOW,
            FindingCategory.BUG,
            "example.py",
            10,
            0.80,
            FindingSource.STATIC_ANALYZER,
        ),

        # Similar finding, different ID
        create_finding(
            "static-eval",
            FindingSeverity.HIGH,
            FindingCategory.SECURITY,
            "auth/login.py",
            2,
            0.90,
            FindingSource.STATIC_ANALYZER,
        ),

        create_finding(
            "ai-eval",
            FindingSeverity.HIGH,
            FindingCategory.SECURITY,
            "auth/login.py",
            2,
            0.95,
            FindingSource.AI_REVIEWER,
        ),

        # Separate finding
        create_finding(
            "performance-1",
            FindingSeverity.MEDIUM,
            FindingCategory.PERFORMANCE,
            "items.py",
            5,
            0.90,
            FindingSource.STATIC_ANALYZER,
        ),
    ]

    aggregator = FindingAggregator()

    result = aggregator.aggregate(findings)

    print("Input findings:", len(findings))
    print("Final findings:", len(result))

    print("\nFinal findings:")

    for finding in result:
        print(
            finding.severity.value,
            "|",
            finding.category.value,
            "|",
            finding.id,
            "| confidence:",
            finding.confidence,
        )


if __name__ == "__main__":
    main()