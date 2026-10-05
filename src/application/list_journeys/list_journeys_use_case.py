import datetime

from domain.journey.journey_repository_interface import JourneyRepositoryInterface

from .list_journeys_dtos import JourneySummaryDTO, ListJourneysOutputDTO

class ListJourneysUseCase:
    def __init__(self, journey_repository: JourneyRepositoryInterface):
        self.journey_repository = journey_repository

    def execute(self) -> ListJourneysOutputDTO:
        summaries = [
            JourneySummaryDTO(
                journey_id=journey.id,
                started_at=journey.route[0].timestamp,
                duration=self._format_duration(journey.route[-1].timestamp - journey.route[0].timestamp),
            )
            for journey in self.journey_repository.find_all()
            if journey.route
        ]
        summaries.sort(key=lambda summary: summary.started_at, reverse=True)

        return ListJourneysOutputDTO(journeys=summaries)

    def _format_duration(self, duration: datetime.timedelta) -> str:
        total = int(duration.total_seconds())
        return f"{total // 3600:02d}:{total % 3600 // 60:02d}:{total % 60:02d}"
