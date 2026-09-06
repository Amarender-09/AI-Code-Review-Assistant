from abc import ABC, abstractmethod

from app.models.finding import Finding


class Analyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        source_code: str,
        file_path: str,
    ) -> list[Finding]:
        pass