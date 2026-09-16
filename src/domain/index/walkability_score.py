from __future__ import annotations

from .walkability_dimension import WalkabilityDimension

class WalkabilityScore:
    @classmethod
    def set(cls, dimension: WalkabilityDimension, value: float) -> WalkabilityScore:
        return WalkabilityScore()

    def calculate(self) -> float:
        return 0.0