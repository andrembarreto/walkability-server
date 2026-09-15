from abc import ABC, abstractmethod

from src.domain.journey.journey import Journey

class JourneyRepositoryInterface(ABC):
    @abstractmethod
    def save(self, journey: Journey) -> Journey:
        pass