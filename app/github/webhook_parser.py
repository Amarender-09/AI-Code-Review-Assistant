from app.models.pull_request import (
    ChangedFile,
    PullRequest,
    Repository,
)


def parse_pull_request_event(payload: dict) -> tuple[Repository, PullRequest, list[ChangedFile]]:
    repository_data = payload["repository"]
    pull_request_data = payload["pull_request"]

    repository = Repository(
        owner=repository_data["owner"]["login"],
        name=repository_data["name"],
        full_name=repository_data["full_name"],
        default_branch=repository_data["default_branch"],
    )

    pull_request = PullRequest(
        number=pull_request_data["number"],
        title=pull_request_data["title"],
        description=pull_request_data.get("body"),
        author=pull_request_data["user"]["login"],
        state=pull_request_data["state"],
        base_branch=pull_request_data["base"]["ref"],
        head_branch=pull_request_data["head"]["ref"],
        base_commit=pull_request_data["base"]["sha"],
        head_commit=pull_request_data["head"]["sha"],
    )

    changed_files = []

    for file_data in payload.get("files", []):
        changed_files.append(
            ChangedFile(
                path=file_data["filename"],
                status=file_data["status"],
                additions=file_data["additions"],
                deletions=file_data["deletions"],
                patch=file_data.get("patch"),
            )
        )

    return repository, pull_request, changed_files