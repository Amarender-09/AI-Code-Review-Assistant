from app.analysis.security import SecurityAnalyzer


def test_security_analyzer_detects_eval():
    source_code = """def login(user_input):
    result = eval(user_input)
    return result
"""

    analyzer = SecurityAnalyzer()

    findings = analyzer.analyze(
        source_code,
        "auth/login.py",
    )

    assert len(findings) == 1

    finding = findings[0]

    assert finding.category.value == "security"
    assert finding.severity.value == "high"
    assert finding.location.file_path == "auth/login.py"
    assert finding.location.start_line == 2
    assert "eval" in finding.title.lower()