from app.models.finding import (
    Finding,
    FindingCategory,
    FindingLocation,
    FindingSeverity,
    FindingSource,
)
from app.reviewers.formatter import ReviewFormatter


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
    evidence='query = "SELECT * FROM users WHERE username = \'" + username + "\'"',
    source=FindingSource.AI_REVIEWER,
)


formatter = ReviewFormatter()

result = formatter.format_review([finding])

print(result)