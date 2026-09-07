from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer


def test_analyzer_runner_runs_all_analyzers():
    source_code = """def process(user_input, items):
    result = eval(user_input)

    for item in items:
        result = result + [item]

    return result
    print("unreachable")
"""

    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    runner = AnalyzerRunner(analyzers)

    findings, warnings = runner.run(
        source_code,
        "example.py",
    )

    assert len(findings) == 3
    assert warnings == []

    categories = {finding.category.value for finding in findings}

    assert categories == {
        "security",
        "bug",
        "performance",
    }