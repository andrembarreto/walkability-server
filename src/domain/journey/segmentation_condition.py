from dataclasses import dataclass

from .segmentation_condition_type import SegmentationConditionType
from .position import Position


@dataclass(frozen=True)
class SegmentationCondition:
    type: SegmentationConditionType
    route: list[Position]
    intensity: float