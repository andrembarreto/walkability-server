from dataclasses import dataclass
from enum import Enum

class EventInfluence(Enum):
    POSITIVE = 1
    NEGATIVE = -1

@dataclass(frozen=True)
class EventItem:
    id: int
    weight: float
    influence: EventInfluence

@dataclass(frozen=True)
class CriteriumItem:
    id: int
    weight: float
    events: list[EventItem]

@dataclass(frozen=True)
class DimensionItem:
    id: int
    criteria: list[CriteriumItem]

def get_dimensions() -> list[DimensionItem]:
    pass

def find_dimension(dimension_id: int) -> DimensionItem:
    pass

def find_event(event_id: int) -> EventItem:
    pass