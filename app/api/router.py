from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.analysis.aggregator import FindingAggregator
from app.analysis.bug import BugAnalyzer
from app.analysis.performance import PerformanceAnalyzer
from app.analysis.runner import AnalyzerRunner
from app.analysis.security import SecurityAnalyzer
from app.github.client import GitHubClient
from app.github.publisher_factory import create_github_publisher
from app.reviewers.ai_review import AIReviewEngine
from app.reviewers.openai_provider import OpenAIProvider
from app.reviewers.validator import FindingValidator
from app.services.code_review_service import CodeReviewService
from app.services.pr_review_service import PRReviewService


router = APIRouter()


class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"


class GitHubPRReviewRequest(BaseModel):
    repository: str
    pull_number: int


def create_code_review_service() -> CodeReviewService:
    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    analyzer_runner = AnalyzerRunner(analyzers)

    ai_provider = OpenAIProvider()
    ai_review_engine = AIReviewEngine(ai_provider)

    aggregator = FindingAggregator()
    validator = FindingValidator()

    return CodeReviewService(
        analyzer_runner=analyzer_runner,
        ai_review_engine=ai_review_engine,
        aggregator=aggregator,
        validator=validator,
    )


def create_pr_review_service() -> PRReviewService:
    analyzers = [
        SecurityAnalyzer(),
        BugAnalyzer(),
        PerformanceAnalyzer(),
    ]

    analyzer_runner = AnalyzerRunner(analyzers)

    ai_provider = OpenAIProvider()
    ai_review_engine = AIReviewEngine(ai_provider)

    aggregator = FindingAggregator()
    validator = FindingValidator()

    github_client = GitHubClient()
    publisher = create_github_publisher()

    return PRReviewService(
        github_client=github_client,
        analyzer_runner=analyzer_runner,
        ai_review_engine=ai_review_engine,
        aggregator=aggregator,
        publisher=publisher,
        validator=validator,
    )


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/review/code")
def review_code(request: CodeReviewRequest):

    if not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty",
        )

    if len(request.code) > 100_000:
        raise HTTPException(
            status_code=400,
            detail="Code is too large. Maximum size is 100,000 characters.",
        )

    supported_languages = {
        "python",
        "javascript",
        "typescript",
    }

    if request.language.lower() not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported language. "
                "Supported languages: "
                "python, javascript, typescript"
            ),
        )

    review_service = create_code_review_service()

    try:
        result = review_service.review_code(
            source_code=request.code,
            language=request.language.lower(),
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Code review failed: {error}",
        )


@router.post("/review/github")
def review_github_pr(request: GitHubPRReviewRequest):

    repository_parts = request.repository.strip().split("/")

    if len(repository_parts) != 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid repository format. "
                "Use owner/repository."
            ),
        )

    owner, repo = repository_parts

    if not owner or not repo:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid repository format. "
                "Use owner/repository."
            ),
        )

    if request.pull_number < 1:
        raise HTTPException(
            status_code=400,
            detail="Pull request number must be greater than 0.",
        )

    review_service = create_pr_review_service()

    try:
        result = review_service.review_pull_request(
            owner=owner,
            repo=repo,
            pull_number=request.pull_number,
        )

        return {
            "repository": request.repository,
            "pull_number": request.pull_number,
            "head_commit": result["head_commit"],
            "changed_files": result["changed_files"],
            "findings": [
                finding.model_dump(mode="json")
                for finding in result["findings"]
            ],
            "warnings": result["warnings"],
            "publish_result": result["publish_result"],
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"GitHub PR review failed: {error}",
        )