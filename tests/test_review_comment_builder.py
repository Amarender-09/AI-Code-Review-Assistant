from app.github.publisher import ReviewCommentBuilder
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
    why_it_matters="An attacker could manipulate the query.",
    recommendation="Use a parameterized SQL query.",
    evidence="username is directly inserted into the query.",
    source=FindingSource.AI_REVIEWER,
)


builder = ReviewCommentBuilder(ReviewFormatter())

comment = builder.build_comment(finding)

print(comment)
print()
print("Path:", comment.path)
print("Line:", comment.line)
print("Side:", comment.side)
print("Body:")
print(comment.body)