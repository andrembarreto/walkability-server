from pydantic import BaseModel
from uuid import UUID
import datetime

class PositionDTO(BaseModel):
    lat: float
    long: float
    time: datetime.datetime

class EventDTO(BaseModel):
    id: int
    pos: PositionDTO

class SaveJourneyInputDTO(BaseModel):
    route: list[PositionDTO]
    events: list[EventDTO]

class SaveJourneyOutputDTO(BaseModel):
    journey_id: UUID