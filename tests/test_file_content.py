from app.github.client import GitHubClient


def main():
    client = GitHubClient()

    pull_request = client.get_pull_request(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    head_commit = pull_request["head"]["sha"]

    content = client.get_file_content(
        owner="octocat",
        repo="Hello-World",
        path="README",
        ref=head_commit,
    )

    print("Head commit:", head_commit)
    print("\nFile content:")
    print(content)


if __name__ == "__main__":
    main()