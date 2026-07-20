from unittest.mock import Mock

from domain.journey.evaluators.evaluator import JourneyEvaluator
from domain.index.walkability_score import WalkabilityScore

from application.evaluate_journey.evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO
from application.evaluate_journey.evaluate_journey_use_case import EvaluateJourneyUseCase


def test_should_delegate_calculation_to_evaluators():
    evaluator_1 = Mock(spec=JourneyEvaluator)
    evaluator_2 = Mock(spec=JourneyEvaluator)

    ev1_score = WalkabilityScore()
    ev2_score = Mock(spec=WalkabilityScore)
    ev2_score.calculate.return_value = 1.0

    evaluator_1.apply.return_value = ev1_score
    evaluator_2.apply.return_value = ev2_score

    use_case = EvaluateJourneyUseCase(evaluators=[evaluator_1, evaluator_2])
    input = EvaluateJourneyInputDTO(events=[], route=[], segmentation_conditions=[])

    result = use_case.execute(input)

    # assert that the use case chains the returned scores
    (params, score), _ = evaluator_1.apply.call_args
    evaluator_2.apply.assert_called_once_with(params, ev1_score)
    assert result.score == 1.0