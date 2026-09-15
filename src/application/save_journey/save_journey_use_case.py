from domain.journey.journey_repository_interface import JourneyRepository
from src.domain.journey.journey import Journey

from .save_journey_dtos import SaveJourneyInputDTO, SaveJourneyOutputDTO

class SaveJourneyUseCase:
    def __init__(self, journey_repository: JourneyRepository):
        self.journey_repository = journey_repository

    def execute(self, input: SaveJourneyInputDTO) -> SaveJourneyOutputDTO:
        if not self._is_valid_journey_data(input):
            raise ValueError("Invalid journey data")

        journey = Journey(route=input.route, events=input.events)
        saved_journey = self.journey_repository.save(journey)
        if not saved_journey:
            raise Exception("Failed to save journey")

        return SaveJourneyOutputDTO(journey_id=saved_journey.id)

    def _is_valid_journey_data(self, journey_data):
        required_fields = ['route', 'events']
        for field in required_fields:
            if field not in journey_data:
                return False
        return True