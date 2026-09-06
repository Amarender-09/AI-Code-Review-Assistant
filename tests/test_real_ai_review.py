from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.openai_provider import OpenAIProvider


provider = OpenAIProvider()
engine = AIReviewEngine(provider)


prompt = """
You are reviewing Python code for security vulnerabilities.

File: login.py

Code:

def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return database.execute(query)

Find genuine security issues.

Return an empty findings array if there are no genuine issues.
"""


result = engine.review(prompt)

print("AIReviewResult:")
print(result)

print("\nNumber of findings:", len(result.findings))

for finding in result.findings:
    print("\nFinding:")
    print("ID:", finding.id)
    print("Category:", finding.category)
    print("Severity:", finding.severity)
    print("Confidence:", finding.confidence)
    print("Title:", finding.title)