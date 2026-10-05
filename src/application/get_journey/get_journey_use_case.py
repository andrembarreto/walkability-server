from domain.index.table import Table
from domain.journey.journey_repository_interface import JourneyRepositoryInterface
from domain.journey.position import Position

from .get_journey_dtos import EventDTO, GetJourneyInputDTO, GetJourneyOutputDTO, PositionDTO

class GetJourneyUseCase:
    def __init__(self, journey_repository: JourneyRepositoryInterface, index_table: Table):
        self.journey_repository = journey_repository
        self.index_table = index_table

    def execute(self, input: GetJourneyInputDTO) -> GetJourneyOutputDTO:
        journey = self.journey_repository.find(input.journey_id)
        if not journey:
            raise ValueError(f"Journey with ID {input.journey_id} not found.")

        return GetJourneyOutputDTO(
            journey_id=journey.id,
            route=[self._to_position_dto(position) for position in journey.route],
            events=[
                EventDTO(
                    id=event.id,
                    description=self._describe_event(event.id),
                    pos=self._to_position_dto(event.position),
                )
                for event in journey.events
            ],
        )

    def _describe_event(self, event_id: int) -> str:
        try:
            return self.index_table.find_event(event_id).name
        except ValueError:
            # evento fora da tabela: mantém a página renderizável
            return f"Evento {event_id}"

    def _to_position_dto(self, position: Position) -> PositionDTO:
        return PositionDTO(lat=position.latitude, long=position.longitude, time=position.timestamp)
