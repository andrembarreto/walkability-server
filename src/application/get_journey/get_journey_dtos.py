from pydantic import BaseModel
from uuid import UUID
import datetime

class GetJourneyInputDTO(BaseModel):
    journey_id: str

class PositionDTO(BaseModel):
    lat: float
    long: float
    time: datetime.datetime

class EventDTO(BaseModel):
    id: int
    description: str
    pos: PositionDTO

class GetJourneyOutputDTO(BaseModel):
    journey_id: UUID
    route: list[PositionDTO]
    events: list[EventDTO]
