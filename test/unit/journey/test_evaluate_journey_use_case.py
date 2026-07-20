from unittest.mock import Mock

from application.evaluate_journey.evaluate_journey_use_case import EvaluateJourneyUseCase
from application.evaluate_journey.evaluate_journey_dtos import *

from domain.journey.evaluators.evaluator import JourneyEvaluator
from domain.journey.position import Position
from domain.journey.event import Event
from domain.journey.event_type import EventType
from domain.journey.segmentation_condition import SegmentationCondition

from domain.index.walkability_score import WalkabilityScore
from domain.index.walkability_parameters import WalkabilityParameters
from domain.journey.segmentation_condition_type import SegmentationConditionType


def test_should_extract_domain_events_from_input():
    position = PositionDTO(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))
    event = EventDTO(type="unknown", position=position)
    input = EvaluateJourneyInputDTO(route=[position], events=[event], segmentation_conditions=[])
    evaluator = Mock(spec=JourneyEvaluator)
    evaluator.apply.return_value = WalkabilityScore()
    use_case = EvaluateJourneyUseCase([evaluator])

    use_case.execute(input)

    args, kwargs = evaluator.apply.call_args
    params: WalkabilityParameters = args[0]

    assert len(params.events) == 1
    assert params.events[0] == Event(
        type=EventType.UNKNOWN,
        position=Position(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))
    )

def test_should_extract_domain_segmentation_conditions_from_input():
    position = PositionDTO(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))
    condition = SegmentationConditionDTO(type="unknown", route=[position], intensity=0.5)
    input = EvaluateJourneyInputDTO(route=[position], events=[], segmentation_conditions=[condition])
    evaluator = Mock(spec=JourneyEvaluator)
    evaluator.apply.return_value = WalkabilityScore()
    use_case = EvaluateJourneyUseCase([evaluator])

    use_case.execute(input)

    args, kwargs = evaluator.apply.call_args
    params: WalkabilityParameters = args[0]

    assert len(params.segmentation_conditions) == 1
    assert params.segmentation_conditions[0] == SegmentationCondition(
        type=SegmentationConditionType.UNKNOWN,
        route=[Position(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))],
        intensity=0.5
    )

def test_should_extract_route_from_input():
    position = PositionDTO(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))
    input = EvaluateJourneyInputDTO(route=[position], events=[], segmentation_conditions=[])
    evaluator = Mock(spec=JourneyEvaluator)
    evaluator.apply.return_value = WalkabilityScore()
    use_case = EvaluateJourneyUseCase([evaluator])

    use_case.execute(input)

    args, kwargs = evaluator.apply.call_args
    params: WalkabilityParameters = args[0]

    assert len(params.route) == 1
    assert params.route[0] == Position(latitude=20.0, longitude=20.0, altitude=100.0, timestamp=datetime.datetime(2000, 1, 1))
