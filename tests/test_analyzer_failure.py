from app.analysis.bug import BugAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer


class BrokenAnalyzer:

    def analyze(
        self,
        source_code: str,
        file_path: str,
    ):
        raise RuntimeError("Simulated analyzer failure")


def test_analyzer_runner_handles_analyzer_failure():
    source_code = """def process(user_input):
    result = eval(user_input)
    return result
"""

    analyzers = [
        SecurityAnalyzer(),
        BrokenAnalyzer(),
        BugAnalyzer(),
    ]

    runner = AnalyzerRunner(analyzers)

    findings, warnings = runner.run(
        source_code,
        "example.py",
    )

    # SecurityAnalyzer should still run successfully.
    assert len(findings) == 1
    assert findings[0].category.value == "security"

    # The broken analyzer should produce a warning,
    # not crash the entire review.
    assert len(warnings) == 1
    assert "BrokenAnalyzer failed" in warnings[0]
    assert "Simulated analyzer failure" in warnings[0]