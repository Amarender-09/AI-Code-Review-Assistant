import json

from fastapi import APIRouter, HTTPException, Request

from app.core.config import GITHUB_WEBHOOK_SECRET
from app.github.webhook_parser import parse_pull_request_event
from app.github.webhook_security import verify_signature
from app.services.review_factory import create_pr_review_service


router = APIRouter()


@router.post("/webhooks/github")
async def github_webhook(request: Request):
    if not GITHUB_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="GitHub webhook secret is not configured",
        )

    payload_body = await request.body()

    signature = request.headers.get(
        "X-Hub-Signature-256"
    )

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

    event_type = request.headers.get(
        "X-GitHub-Event"
    )

    if event_type != "pull_request":
        return {
            "message": "GitHub event ignored",
            "event_type": event_type,
        }

    action = payload.get("action")

    if action not in {
        "opened",
        "synchronize",
        "reopened",
    }:
        return {
            "message": "Pull request action ignored",
            "action": action,
        }

    try:
        repository, pull_request, changed_files = (
            parse_pull_request_event(payload)
        )
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pull request payload: {error}",
        )

    review_service = create_pr_review_service()

    try:
        result = review_service.review_pull_request(
            owner=repository.owner,
            repo=repository.name,
            pull_number=pull_request.number,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Pull request review failed: {error}",
        )

    return {
        "message": "Pull request review completed",
        "repository": repository.full_name,
        "pull_request": pull_request.number,
        "changed_files_from_webhook": len(changed_files),
        "review": result,
    }