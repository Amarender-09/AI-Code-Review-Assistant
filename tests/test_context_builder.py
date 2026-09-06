from app.github.client import GitHubClient
from app.github.context_builder import build_code_context
from app.github.adapters import github_files_to_changed_files


def main():
    client = GitHubClient()

    file_data = client.get_pull_request_files(
        owner="octocat",
        repo="Hello-World",
        pull_number=1,
    )

    changed_files = github_files_to_changed_files(file_data)

    for changed_file in changed_files:
        source_code = client.get_file_content(
            owner="octocat",
            repo="Hello-World",
            path=changed_file.path,
            ref="7044a8a032e85b6ab611033b2ac8af7ce85805b2",
        )

        context = build_code_context(
            changed_file,
            source_code,
        )

        print("File:", context.file_path)
        print("Language:", context.language)

        print("\nChanged code:")
        print(context.changed_code)

        print("\nSurrounding source code:")
        print(context.surrounding_code)


if __name__ == "__main__":
    main()