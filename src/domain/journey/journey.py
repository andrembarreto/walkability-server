from uuid import UUID
from dataclasses import dataclass

from .position import Position
from .event import Event

@dataclass
class Journey:
    id: UUID
    route: list[Position]
    events: list[Event]