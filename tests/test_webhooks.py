import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_signature(payload: bytes, secret: str) -> str:
    digest = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return f"sha256={digest}"


def test_webhook_rejects_missing_secret(monkeypatch):
    monkeypatch.setattr(
        "app.api.webhooks.GITHUB_WEBHOOK_SECRET",
        "",
    )

    payload = b"{}"

    response = client.post(
        "/webhooks/github",
        content=payload,
    )

    assert response.status_code == 500


def test_webhook_rejects_invalid_signature(monkeypatch):
    secret = "test-secret"

    monkeypatch.setattr(
        "app.api.webhooks.GITHUB_WEBHOOK_SECRET",
        secret,
    )

    payload = b'{"action":"opened"}'

    response = client.post(
        "/webhooks/github",
        content=payload,
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=invalid",
        },
    )

    assert response.status_code == 403


def test_webhook_ignores_non_pull_request_event(monkeypatch):
    secret = "test-secret"

    monkeypatch.setattr(
        "app.api.webhooks.GITHUB_WEBHOOK_SECRET",
        secret,
    )

    payload = b'{"action":"opened"}'
    signature = create_signature(payload, secret)

    response = client.post(
        "/webhooks/github",
        content=payload,
        headers={
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": signature,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "GitHub event ignored"
    assert data["event_type"] == "push"


def test_webhook_processes_valid_pull_request(
    monkeypatch,
):
    secret = "test-secret"

    monkeypatch.setattr(
        "app.api.webhooks.GITHUB_WEBHOOK_SECRET",
        secret,
    )

    class FakeReviewService:
        def review_pull_request(
            self,
            owner,
            repo,
            pull_number,
        ):
            assert owner == "test-owner"
            assert repo == "test-repo"
            assert pull_number == 123

            return {
                "pull_number": 123,
                "head_commit": "abc123",
                "changed_files": 1,
                "findings": [],
                "warnings": [],
                "publish_result": {
                    "published": False,
                    "mode": "dry_run",
                },
            }

    monkeypatch.setattr(
        "app.api.webhooks.create_pr_review_service",
        lambda: FakeReviewService(),
    )

    payload = {
        "action": "opened",
        "repository": {
            "owner": {
                "login": "test-owner",
            },
            "name": "test-repo",
            "full_name": "test-owner/test-repo",
            "default_branch": "main",
        },
        "pull_request": {
            "number": 123,
            "title": "Test PR",
            "body": "Test pull request",
            "user": {
                "login": "test-user",
            },
            "state": "open",
            "base": {
                "ref": "main",
                "sha": "base123",
            },
            "head": {
                "ref": "feature",
                "sha": "abc123",
            },
        },
    }

    payload_bytes = json.dumps(payload).encode()
    signature = create_signature(
        payload_bytes,
        secret,
    )

    response = client.post(
        "/webhooks/github",
        content=payload_bytes,
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": signature,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Pull request received"
    assert data["repository"] == "test-owner/test-repo"
    assert data["pull_request"] == 123
    assert data["changed_files_from_webhook"] == 0