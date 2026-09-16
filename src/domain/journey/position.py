from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Position:
    latitude: float
    longitude: float
    timestamp: datetime