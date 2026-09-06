from app.analysis.bug import BugAnalyzer


def main():
    source_code = """def calculate():
    value = 10
    return value
    print("This never runs")
"""

    analyzer = BugAnalyzer()

    findings = analyzer.analyze(
        source_code,
        "calculator.py",
    )

    print("Findings:", len(findings))

    for finding in findings:
        print(finding.model_dump())


if __name__ == "__main__":
    main()