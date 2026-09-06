from app.models.pull_request import (
    ChangedFile,
    PullRequest,
    Repository,
)


def github_pr_to_repository(data: dict) -> Repository:
    return Repository(
        owner=data["base"]["repo"]["owner"]["login"],
        name=data["base"]["repo"]["name"],
        full_name=data["base"]["repo"]["full_name"],
        default_branch=data["base"]["repo"]["default_branch"],
    )


def github_pr_to_pull_request(data: dict) -> PullRequest:
    return PullRequest(
        number=data["number"],
        title=data["title"],
        description=data.get("body"),
        author=data["user"]["login"],
        state=data["state"],
        base_branch=data["base"]["ref"],
        head_branch=data["head"]["ref"],
        base_commit=data["base"]["sha"],
        head_commit=data["head"]["sha"],
    )


def github_file_to_changed_file(data: dict) -> ChangedFile:
    return ChangedFile(
        path=data["filename"],
        status=data["status"],
        additions=data["additions"],
        deletions=data["deletions"],
        patch=data.get("patch"),
    )


def github_files_to_changed_files(
    data: list[dict],
) -> list[ChangedFile]:
    return [
        github_file_to_changed_file(file_data)
        for file_data in data
    ]
