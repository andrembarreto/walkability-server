from domain.journey.evaluators.evaluator import JourneyEvaluator
from domain.journey.position import Position
from domain.journey.event import Event
from domain.journey.event_type import EventType
from domain.journey.segmentation_condition_type import SegmentationConditionType
from domain.journey.segmentation_condition import SegmentationCondition

from domain.index.walkability_parameters import WalkabilityParameters
from domain.index.walkability_score import WalkabilityScore

from .evaluate_journey_dtos import (
    EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO, EventDTO,
    PositionDTO, SegmentationConditionDTO
)

class EvaluateJourneyUseCase:
    def __init__(self, evaluators: list[JourneyEvaluator]):
        self.evaluators = evaluators

    def execute(self, input: EvaluateJourneyInputDTO) -> EvaluateJourneyOutputDTO:
        parameters = self._extract_parameters_from_input(input)

        score = WalkabilityScore()

        for evaluator in self.evaluators:
            score = evaluator.apply(parameters, score)

        return EvaluateJourneyOutputDTO(score=score.calculate())

    def _extract_parameters_from_input(self, input: EvaluateJourneyInputDTO) -> WalkabilityParameters:
        return WalkabilityParameters(
            route=[self._position_from_dto(position_dto) for position_dto in input.route],
            events=[self._event_from_dto(event_dto) for event_dto in input.events],
            segmentation_conditions=[self._segmentation_condition_from_dto(condition_dto) for condition_dto in input.segmentation_conditions]
        )

    def _event_from_dto(self, event_dto: EventDTO) -> Event:
        return Event(
            type=EventType(event_dto.type),
            position=self._position_from_dto(event_dto.position)
        )

    def _segmentation_condition_from_dto(self, condition_dto: SegmentationConditionDTO) -> SegmentationCondition:
        return SegmentationCondition(
            type=SegmentationConditionType(condition_dto.type),
            route=[self._position_from_dto(pos) for pos in condition_dto.route],
            intensity=condition_dto.intensity
        )

    def _position_from_dto(self, position_dto: PositionDTO) -> Position:
        return Position(
            latitude=position_dto.latitude,
            longitude=position_dto.longitude,
            altitude=position_dto.altitude,
            timestamp=position_dto.timestamp
        )