import uuid

from domain.journey.journey_repository_interface import JourneyRepositoryInterface
from domain.journey.position import Position
from domain.journey.event import Event
from domain.journey.journey import Journey

from .save_journey_dtos import SaveJourneyInputDTO, SaveJourneyOutputDTO, PositionDTO, EventDTO

class SaveJourneyUseCase:
    def __init__(self, journey_repository: JourneyRepositoryInterface):
        self.journey_repository = journey_repository

    def execute(self, input: SaveJourneyInputDTO) -> SaveJourneyOutputDTO:
        route = [self.position_from_dto(position_dto) for position_dto in input.route]
        events = [self.event_from_dto(event_dto) for event_dto in input.events]
        journey = Journey(id=uuid.uuid4(), route=route, events=events)
        saved_journey = self.journey_repository.save(journey)
        if not saved_journey:
            raise Exception("Failed to save journey")

        return SaveJourneyOutputDTO(journey_id=saved_journey.id)

    def event_from_dto(self, event_dto: EventDTO) -> Event:
        return Event(
            id=event_dto.id,
            position=self.position_from_dto(event_dto.pos)
        )

    def position_from_dto(self, position_dto: PositionDTO) -> Position:
        return Position(
            latitude=position_dto.lat,
            longitude=position_dto.long,
            timestamp=position_dto.time
        )