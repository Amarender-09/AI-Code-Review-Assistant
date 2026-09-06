from app.github.adapters import (
    github_files_to_changed_files,
    github_pr_to_pull_request,
    github_pr_to_repository,
)
from app.github.client import GitHubClient


def main():
    client = GitHubClient()

    pr_data = client.get_pull_request(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    file_data = client.get_pull_request_files(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    repository = github_pr_to_repository(pr_data)
    pull_request = github_pr_to_pull_request(pr_data)
    changed_files = github_files_to_changed_files(file_data)

    print("Repository:")
    print(repository.model_dump())

    print("\nPull Request:")
    print(pull_request.model_dump())

    print("\nChanged Files:")
    for changed_file in changed_files:
        print(changed_file.model_dump())


if __name__ == "__main__":
    main()
    