import base64
import certifi
import json
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import (
    GITHUB_API_URL,
    GITHUB_API_VERSION,
    GITHUB_TOKEN,
)


class GitHubAPIError(Exception):
    """Raised when a GitHub API request fails."""


class GitHubClient:
    def __init__(self, token: str | None = GITHUB_TOKEN):
        self.token = token

    def _request(self, method: str, path: str) -> dict | list:
        url = f"{GITHUB_API_URL}{path}"

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = Request(
            url,
            method=method,
            headers=headers,
        )

        ssl_context = ssl.create_default_context(
            cafile=certifi.where()
        )

        try:
            with urlopen(
                request,
                timeout=15,
                context=ssl_context,
            ) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body)

        except HTTPError as error:
            error_body = error.read().decode("utf-8")

            raise GitHubAPIError(
                f"GitHub API returned HTTP {error.code}: {error_body}"
            ) from error

        except URLError as error:
            raise GitHubAPIError(
                f"Could not connect to GitHub API: {error.reason}"
            ) from error

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{GITHUB_API_URL}{path}"

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "Content-Type": "application/json",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        body = json.dumps(payload).encode("utf-8")

        request = Request(
            url,
            data=body,
            method="POST",
            headers=headers,
        )

        ssl_context = ssl.create_default_context(
            cafile=certifi.where()
        )

        try:
            with urlopen(
                request,
                timeout=15,
                context=ssl_context,
            ) as response:

                response_body = response.read().decode("utf-8")
                result = json.loads(response_body)

                if not isinstance(result, dict):
                    raise GitHubAPIError(
                        "GitHub returned an unexpected POST response"
                    )

                return result

        except HTTPError as error:
            error_body = error.read().decode("utf-8")

            raise GitHubAPIError(
                f"GitHub API returned HTTP {error.code}: {error_body}"
            ) from error

        except URLError as error:
            raise GitHubAPIError(
                f"Could not connect to GitHub API: {error.reason}"
            ) from error

    def get_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> dict:

        return self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}",
        )

    def get_pull_request_files(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> list:

        result = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/files",
        )

        if not isinstance(result, list):
            raise GitHubAPIError(
                "GitHub returned an unexpected response for pull request files"
            )

        return result

    def get_pull_request_commits(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> list:

        result = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/commits",
        )

        if not isinstance(result, list):
            raise GitHubAPIError(
                "GitHub returned an unexpected response for pull request commits"
            )

        return result

    def get_file_content(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: str,
    ) -> str:

        result = self._request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{path}?ref={ref}",
        )

        if not isinstance(result, dict):
            raise GitHubAPIError(
                "GitHub returned an unexpected response for file content"
            )

        if result.get("encoding") != "base64":
            raise GitHubAPIError(
                "GitHub returned file content in an unsupported encoding"
            )

        content = result.get("content")

        if not isinstance(content, str):
            raise GitHubAPIError(
                "GitHub did not return file content"
            )

        try:
            decoded_content = base64.b64decode(content).decode("utf-8")

        except (ValueError, UnicodeDecodeError) as error:
            raise GitHubAPIError(
                "Could not decode GitHub file content"
            ) from error

        return decoded_content

    def create_pull_request_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        commit_id: str,
        comments: list[dict],
    ) -> dict:

        payload = {
            "commit_id": commit_id,
            "event": "COMMENT",
            "comments": comments,
        }

        return self._post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
            payload,
        )