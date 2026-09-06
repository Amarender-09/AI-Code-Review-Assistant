from app.github.diff_parser import (
    extract_surrounding_code,
    get_changed_line_ranges,
)


def main():
    patch = """@@ -10,3 +10,5 @@
+def login():
+    return True
"""

    ranges = get_changed_line_ranges(patch)

    print("Changed ranges:")
    print(ranges)

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

    surrounding_code = extract_surrounding_code(
        source_code,
        ranges,
        context_lines=2,
    )

    print("\nSurrounding code:")
    print(surrounding_code)


if __name__ == "__main__":
    main()