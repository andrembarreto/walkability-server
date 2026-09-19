from domain.index import index_calculator
from domain.journey.journey_repository_interface import JourneyRepositoryInterface

from .evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO

class EvaluateJourneyUseCase:
    def __init__(self, journey_repository: JourneyRepositoryInterface):
        self.journey_repository = journey_repository

    def execute(self, input: EvaluateJourneyInputDTO) -> EvaluateJourneyOutputDTO:
        journey = self.journey_repository.find(input.journey_id)
        score = index_calculator.calculate_index_score(route=journey.route, events=journey.events)
        return EvaluateJourneyOutputDTO(global_score=score.global_score, dimension_scores=score.dimension_scores)