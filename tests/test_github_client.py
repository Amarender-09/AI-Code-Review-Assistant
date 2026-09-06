from app.github.client import GitHubClient


def main():
    client = GitHubClient()

    repository = client.get_pull_request(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    print("Repository:", repository["base"]["repo"]["full_name"])
    print("PR number:", repository["number"])
    print("PR title:", repository["title"])

    files = client.get_pull_request_files(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    print("Changed files:", len(files))

    commits = client.get_pull_request_commits(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    print("Commits:", len(commits))


if __name__ == "__main__":
    main()