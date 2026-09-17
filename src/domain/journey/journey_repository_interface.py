from abc import ABC, abstractmethod
from uuid import UUID

from .journey import Journey

class JourneyRepositoryInterface(ABC):
    @abstractmethod
    def save(self, journey: Journey) -> Journey:
        pass

    def find(self, journey_id: UUID) -> Journey:
        pass