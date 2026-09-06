
from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.coordinator import ReviewCoordinator
from app.reviewers.openai_provider import OpenAIProvider


analyzer_runner = AnalyzerRunner(
    [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]
)

ai_provider = OpenAIProvider()
ai_review_engine = AIReviewEngine(ai_provider)

aggregator = FindingAggregator()

coordinator = ReviewCoordinator(
    analyzer_runner=analyzer_runner,
    ai_review_engine=ai_review_engine,
    aggregator=aggregator,
)


source_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return database.execute(query)

def calculate(items):
    result = []
    for item in items:
        result = result + [item]
    return result

def example():
    return 10
    print("unreachable")
"""


prompt = """
You are an AI code reviewer.

Review the following Python code for genuine:
- security issues
- bugs
- performance problems
- code quality issues
- testing concerns

Only report meaningful issues.

File: example.py

Code:
""" + source_code


findings, warnings = coordinator.review(
    source_code=source_code,
    file_path="example.py",
    ai_prompt=prompt,
)


print("Final findings:", len(findings))
print("Warnings:", warnings)

for finding in findings:
    print("\n--- Finding ---")
    print("ID:", finding.id)
    print("Category:", finding.category)
    print("Severity:", finding.severity)
    print("Confidence:", finding.confidence)
    print("Title:", finding.title)