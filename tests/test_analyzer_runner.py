from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer


def main():

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

    print("Findings:", len(findings))

    for finding in findings:
        print(
            finding.category.value,
            "|",
            finding.title,
            "| line:",
            finding.location.start_line,
        )

    print("\nWarnings:", len(warnings))

    for warning in warnings:
        print(warning)


if __name__ == "__main__":
    main()