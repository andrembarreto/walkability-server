from dataclasses import dataclass

from domain.journey.event import Event
from domain.journey.position import Position
from domain.journey.segmentation_condition import SegmentationCondition


@dataclass(frozen=True)
class WalkabilityParameters:
    route: list[Position]
    events: list[Event]
    segmentation_conditions: list[SegmentationCondition]
