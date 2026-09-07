from app.analysis.performance import PerformanceAnalyzer


def test_performance_analyzer_detects_list_concatenation():
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

    assert len(findings) == 1

    finding = findings[0]

    assert finding.category.value == "performance"
    assert finding.severity.value == "medium"
    assert finding.location.file_path == "items.py"
    assert finding.location.start_line == 5
    assert "concatenation" in finding.title.lower()