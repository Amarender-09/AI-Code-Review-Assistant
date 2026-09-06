from app.models.repository_context import RepositoryContext
from app.models.pull_request import ChangedFile, Repository


def main():

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

    print("Repository Context:")
    print(context.model_dump())


if __name__ == "__main__":
    main()