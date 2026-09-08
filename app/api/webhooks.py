import json

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from app.core.config import GITHUB_WEBHOOK_SECRET
from app.github.webhook_parser import parse_pull_request_event
from app.github.webhook_security import verify_signature
from app.services.review_factory import create_pr_review_service


router = APIRouter()


def process_pull_request_review(
    owner: str,
    repo: str,
    pull_number: int,
):
    review_service = create_pr_review_service()

    review_service.review_pull_request(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
    )


@router.post("/webhooks/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
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

    background_tasks.add_task(
        process_pull_request_review,
        repository.owner,
        repository.name,
        pull_request.number,
    )

    return {
        "message": "Pull request received",
        "repository": repository.full_name,
        "pull_request": pull_request.number,
        "changed_files_from_webhook": len(changed_files),
    }