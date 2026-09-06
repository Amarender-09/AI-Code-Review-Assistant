from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate_review(
        self,
        prompt: str,
    ) -> str:
        pass