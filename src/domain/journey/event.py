from dataclasses import dataclass

from .event_type import EventType
from .position import Position


@dataclass(frozen=True)
class Event:
    type: EventType
    position: Position