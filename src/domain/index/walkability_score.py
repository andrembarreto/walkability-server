from __future__ import annotations

from domain.index.walkability_dimension import WalkabilityDimension


class WalkabilityScore:
    @classmethod
    def set(cls, dimension: WalkabilityDimension, value: float) -> WalkabilityScore:
        pass

    def calculate(self) -> float:
        pass