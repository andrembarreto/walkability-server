from pydantic import BaseModel
import datetime

class PositionDTO(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    timestamp: datetime.datetime


class EventDTO(BaseModel):
    type: str
    position: PositionDTO


class SegmentationConditionDTO(BaseModel):
    type: str
    route: list[PositionDTO]
    intensity: float


class EvaluateJourneyInputDTO(BaseModel):
    route: list[PositionDTO]
    events: list[EventDTO]
    segmentation_conditions: list[SegmentationConditionDTO]


class EvaluateJourneyOutputDTO(BaseModel):
    score: float