from pydantic import BaseModel
from uuid import UUID
import datetime

class PositionDTO(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime.datetime

class EventDTO(BaseModel):
    id: int
    position: PositionDTO

class SaveJourneyInputDTO(BaseModel):
    route: list[PositionDTO]
    events: list[EventDTO]

class SaveJourneyOutputDTO(BaseModel):
    journey_id: UUID