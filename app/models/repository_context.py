from pydantic import BaseModel

from app.models.pull_request import ChangedFile, Repository


class RepositoryContext(BaseModel):
    repository: Repository
    changed_files: list[ChangedFile]
    file_paths: list[str]