from uuid import UUID

from .position import Position
from .event import Event

class Journey:
    id: UUID
    route: list[Position]
    events: list[Event]