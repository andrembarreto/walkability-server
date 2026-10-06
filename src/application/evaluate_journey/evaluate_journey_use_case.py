from domain.index.calculator import Calculator, Score
from domain.index.segmentation import RouteSplitter
from domain.index.table import Table
from domain.journey.journey_repository_interface import JourneyRepositoryInterface

from .evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO

class EvaluateJourneyUseCase:
    def __init__(self, journey_repository: JourneyRepositoryInterface, index_table: Table, split_route: RouteSplitter):
        self.journey_repository = journey_repository
        self.index_table = index_table
        self.split_route = split_route

    def execute(self, input: EvaluateJourneyInputDTO) -> EvaluateJourneyOutputDTO:
        journey = self.journey_repository.find(input.journey_id)
        if not journey:
            raise ValueError(f"Journey with ID {input.journey_id} not found.")

        calculator = Calculator(self.index_table, self.split_route)
        score: Score = calculator.calculate(route=journey.route, events=journey.events)

        return EvaluateJourneyOutputDTO(
            global_score=score.global_score,
            dimension_scores=score.dimension_scores
        )