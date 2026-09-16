from abc import ABC, abstractmethod

from .journey import Journey

class JourneyRepositoryInterface(ABC):
    @abstractmethod
    def save(self, journey: Journey) -> Journey:
        pass