from __future__ import annotations

from .walkability_dimension import WalkabilityDimension

from domain.journey.position import Position
from domain.journey.event import Event
from domain.journey.segmentation_condition import SegmentationCondition

class WalkabilityScore:
    @classmethod
    def set(cls, dimension: WalkabilityDimension, value: float) -> WalkabilityScore:
        return WalkabilityScore()

    def calculate(self) -> float:
        return 0.0