import json

from fastapi import APIRouter, HTTPException, Request

from app.core.config import GITHUB_WEBHOOK_SECRET
from app.github.webhook_security import verify_signature
from app.github.webhook_parser import parse_pull_request_event


router = APIRouter()


@router.post("/webhooks/github")
async def github_webhook(request: Request):
    if not GITHUB_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="GitHub webhook secret is not configured",
        )

    payload_body = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(
        payload_body,
        GITHUB_WEBHOOK_SECRET,
        signature,
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature",
        )

    try:
        payload = json.loads(payload_body)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        )

    event_type = request.headers.get("X-GitHub-Event")

    if event_type != "pull_request":
        return {
            "message": "GitHub event ignored",
            "event_type": event_type,
        }

    action = payload.get("action")

    if action not in {"opened", "synchronize", "reopened"}:
        return {
            "message": "Pull request action ignored",
            "action": action,
        }

    try:
        repository, pull_request, changed_files = parse_pull_request_event(
            payload
        )
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pull request payload: {error}",
        )

    return {
        "message": "Pull request parsed successfully",
        "repository": repository.model_dump(),
        "pull_request": pull_request.model_dump(),
        "changed_files": [
            changed_file.model_dump()
            for changed_file in changed_files
        ],
    }