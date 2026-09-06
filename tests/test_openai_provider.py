from app.reviewers.openai_provider import OpenAIProvider


provider = OpenAIProvider()

response = provider.generate_review(
    """
You are a security-focused code reviewer.

Review this Python code for security vulnerabilities:

def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return database.execute(query)

Return a finding if there is a genuine security issue.
If there is no genuine issue, return an empty findings array.

The finding must identify the security problem, explain why it matters,
and recommend how to fix it.
"""
)

print("OpenAI response:")
print(response)