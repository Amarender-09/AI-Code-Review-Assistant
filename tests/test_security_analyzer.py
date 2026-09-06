from app.analysis.security import SecurityAnalyzer


def main():
    source_code = """def login(user_input):
    result = eval(user_input)
    return result
"""

    analyzer = SecurityAnalyzer()

    findings = analyzer.analyze(
        source_code,
        "auth/login.py",
    )

    print("Findings:", len(findings))

    for finding in findings:
        print(finding.model_dump())


if __name__ == "__main__":
    main()