from src.domain.journey.evaluators.evaluator import JourneyEvaluator
from .evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO


class EvaluateJourneyUseCase:
    def __init__(self, evaluators: list[JourneyEvaluator]):
        self.evaluators = evaluators

    def execute(self, input_dto: EvaluateJourneyInputDTO) -> EvaluateJourneyOutputDTO:
        pass