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


def main():

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

    print("Findings:", len(findings))

    for finding in findings:
        print(
            finding.category.value,
            "|",
            finding.title,
        )

    print("\nWarnings:", len(warnings))

    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    main()