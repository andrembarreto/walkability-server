from pydantic import BaseModel

class EvaluateJourneyInputDTO(BaseModel):
    journey_id: str

class EvaluateJourneyOutputDTO(BaseModel):
    global_score: float
    dimension_scores: dict[int, float]