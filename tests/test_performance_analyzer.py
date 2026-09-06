from app.analysis.performance import PerformanceAnalyzer


def main():
    source_code = """def build_items(items):
    result = []

    for item in items:
        result = result + [item]

    return result
"""

    analyzer = PerformanceAnalyzer()

    findings = analyzer.analyze(
        source_code,
        "items.py",
    )

    print("Findings:", len(findings))

    for finding in findings:
        print(finding.model_dump())


if __name__ == "__main__":
    main()