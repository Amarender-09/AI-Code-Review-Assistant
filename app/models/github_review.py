from pydantic import BaseModel


class GitHubReviewComment(BaseModel):
    path: str
    line: int
    side: str = "RIGHT"
    body: str