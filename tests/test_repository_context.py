from app.models.repository_context import RepositoryContext
from app.models.pull_request import ChangedFile, Repository


def test_repository_context_model():
    repository = Repository(
        owner="example",
        name="demo-project",
        full_name="example/demo-project",
        default_branch="main",
    )

    changed_files = [
        ChangedFile(
            path="auth/login.py",
            status="modified",
            additions=10,
            deletions=3,
            patch=None,
        ),
        ChangedFile(
            path="tests/test_login.py",
            status="added",
            additions=20,
            deletions=0,
            patch=None,
        ),
    ]

    context = RepositoryContext(
        repository=repository,
        changed_files=changed_files,
        file_paths=[
            "auth/login.py",
            "tests/test_login.py",
            "auth/user.py",
            "README.md",
        ],
    )

    assert context.repository.full_name == "example/demo-project"
    assert context.repository.default_branch == "main"

    assert len(context.changed_files) == 2
    assert context.changed_files[0].path == "auth/login.py"
    assert context.changed_files[1].path == "tests/test_login.py"

    assert context.file_paths == [
        "auth/login.py",
        "tests/test_login.py",
        "auth/user.py",
        "README.md",
    ]