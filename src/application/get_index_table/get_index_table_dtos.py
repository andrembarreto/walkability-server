from pydantic import BaseModel

class EventDTO(BaseModel):
    id: int
    description: str

class DimensionDTO(BaseModel):
    id: int
    name: str
    events: list[EventDTO]

class GetIndexTableOutputDTO(BaseModel):
    dimensions: list[DimensionDTO]