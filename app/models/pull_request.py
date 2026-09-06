from pydantic import BaseModel


class Repository(BaseModel):
    owner: str
    name: str
    full_name: str
    default_branch: str


class PullRequest(BaseModel):
    number: int
    title: str
    description: str | None
    author: str
    state: str
    base_branch: str
    head_branch: str
    base_commit: str
    head_commit: str


class ChangedFile(BaseModel):
    path: str
    status: str
    additions: int
    deletions: int
    patch: str | None = None