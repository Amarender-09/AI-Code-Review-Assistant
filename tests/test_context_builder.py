from app.github.context_builder import build_code_context
from app.models.pull_request import ChangedFile


def test_context_builder_builds_python_context():
    changed_file = ChangedFile(
        path="auth/login.py",
        status="modified",
        additions=2,
        deletions=1,
        patch="""@@ -8,3 +8,5 @@
+def login():
+    return True
""",
    )

    source_code = """line 1
line 2
line 3
line 4
line 5
line 6
line 7
def login():
    return True
line 10
line 11
line 12
"""

    context = build_code_context(
        changed_file,
        source_code,
    )

    assert context.file_path == "auth/login.py"
    assert context.language == "python"
    assert context.changed_code == changed_file.patch

    assert "line 6" in context.surrounding_code
    assert "def login():" in context.surrounding_code
    assert "return True" in context.surrounding_code

    assert context.related_tests == []