from domain.index.walkability_score import WalkabilityScore
from domain.index.walkability_parameters import WalkabilityParameters


class JourneyEvaluator:
    def apply(self, parameters: WalkabilityParameters, score: WalkabilityScore) -> WalkabilityScore:
        raise NotImplementedError("Subclasses must implement the apply method.")