from app.github.adapters import (
    github_files_to_changed_files,
    github_pr_to_pull_request,
    github_pr_to_repository,
)


def test_github_pr_adapter_converts_pull_request():
    pr_data = {
        "number": 42,
        "title": "Fix authentication",
        "body": "Improve login security.",
        "state": "open",
        "user": {
            "login": "developer"
        },
        "base": {
            "ref": "main",
            "sha": "base123",
            "repo": {
                "owner": {
                    "login": "example"
                },
                "name": "demo-project",
                "full_name": "example/demo-project",
                "default_branch": "main",
            },
        },
        "head": {
            "ref": "feature/auth",
            "sha": "head456",
        },
    }

    repository = github_pr_to_repository(pr_data)
    pull_request = github_pr_to_pull_request(pr_data)

    assert repository.owner == "example"
    assert repository.name == "demo-project"
    assert repository.full_name == "example/demo-project"
    assert repository.default_branch == "main"

    assert pull_request.number == 42
    assert pull_request.title == "Fix authentication"
    assert pull_request.description == "Improve login security."
    assert pull_request.author == "developer"
    assert pull_request.state == "open"
    assert pull_request.base_branch == "main"
    assert pull_request.head_branch == "feature/auth"
    assert pull_request.base_commit == "base123"
    assert pull_request.head_commit == "head456"


def test_github_file_adapter_converts_changed_files():
    file_data = [
        {
            "filename": "auth/login.py",
            "status": "modified",
            "additions": 10,
            "deletions": 3,
            "patch": "@@ -1,3 +1,10 @@",
        },
        {
            "filename": "tests/test_login.py",
            "status": "added",
            "additions": 20,
            "deletions": 0,
            "patch": None,
        },
    ]

    changed_files = github_files_to_changed_files(file_data)

    assert len(changed_files) == 2

    first_file = changed_files[0]

    assert first_file.path == "auth/login.py"
    assert first_file.status == "modified"
    assert first_file.additions == 10
    assert first_file.deletions == 3
    assert first_file.patch == "@@ -1,3 +1,10 @@"

    second_file = changed_files[1]

    assert second_file.path == "tests/test_login.py"
    assert second_file.status == "added"
    assert second_file.additions == 20
    assert second_file.deletions == 0
    assert second_file.patch is None
    