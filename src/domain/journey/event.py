from dataclasses import dataclass

from .position import Position


@dataclass(frozen=True)
class Event:
    id: int
    position: Position