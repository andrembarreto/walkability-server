from pydantic import BaseModel
from uuid import UUID
import datetime

class JourneySummaryDTO(BaseModel):
    journey_id: UUID
    started_at: datetime.datetime
    duration: str  # "hh:mm:ss"

class ListJourneysOutputDTO(BaseModel):
    journeys: list[JourneySummaryDTO]
