from app.github.diff_parser import (
    extract_surrounding_code,
    get_changed_line_ranges,
)


def test_get_changed_line_ranges():
    patch = """@@ -10,3 +10,5 @@
+def login():
+    return True
"""

    ranges = get_changed_line_ranges(patch)

    assert ranges == [(10, 5)]


def test_extract_surrounding_code():
    source_code = """line 1
line 2
line 3
line 4
line 5
line 6
line 7
line 8
line 9
def login():
    return True
line 12
line 13
line 14
line 15
"""

    changed_ranges = [(10, 2)]

    surrounding_code = extract_surrounding_code(
        source_code,
        changed_ranges,
        context_lines=2,
    )

    expected = """line 8
line 9
def login():
    return True
line 12
line 13"""

    assert surrounding_code == expected