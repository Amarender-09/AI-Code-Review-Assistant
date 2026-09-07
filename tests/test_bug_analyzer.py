from app.analysis.bug import BugAnalyzer


def test_bug_analyzer_detects_unreachable_code():
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

    assert len(findings) == 1

    finding = findings[0]

    assert finding.category.value == "bug"
    assert finding.severity.value == "medium"
    assert finding.location.file_path == "calculator.py"
    assert finding.location.start_line == 4
    assert "unreachable" in finding.title.lower()