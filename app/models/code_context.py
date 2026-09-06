from pydantic import BaseModel


class CodeContext(BaseModel):
    file_path: str
    language: str
    changed_code: str
    surrounding_code: str | None = None
    related_tests: list[str] = []