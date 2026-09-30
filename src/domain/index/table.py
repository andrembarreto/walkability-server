from pydantic import BaseModel
import json


class EventItem(BaseModel):
    id: int
    weight: float

class CriteriumItem(BaseModel):
    id: int
    weight: float
    events: list[EventItem]

class DimensionItem(BaseModel):
    id: int
    criteria: list[CriteriumItem]

class Table:
    def __init__(self, source: str):
        self._dimensions = self._load_dimensions(source)

    @property
    def dimensions(self) -> list[DimensionItem]:
        return self._dimensions

    def find_dimension(self, dimension_id: int) -> DimensionItem:
        for dimension in self._dimensions:
            if dimension.id == dimension_id:
                return dimension
        raise ValueError(f"Dimension with ID {dimension_id} not found.")

    def find_event(self, event_id: int) -> EventItem:
        for dimension in self._dimensions:
            for criterium in dimension.criteria:
                for event in criterium.events:
                    if event.id == event_id:
                        return event
        raise ValueError(f"Event with ID {event_id} not found.")

    def _load_dimensions(self, source: str) -> list[DimensionItem]:
        with open(source, 'r') as file:
            data = json.load(file)
            return [self._parse_dimension(d) for d in data['dimensions']]

    def _parse_dimension(self, data: dict) -> DimensionItem:
        return DimensionItem(
            id=self._parse_id(data['id']),
            criteria=[self._parse_criterium(c) for c in data['criteria']]
        )

    def _parse_criterium(self, data: dict) -> CriteriumItem:
        return CriteriumItem(
            id=self._parse_id(data['id']),
            weight=data.get('weight', 1.0),
            events=[self._parse_event(e) for e in data['events']]
        )

    def _parse_event(self, data: dict) -> EventItem:
        return EventItem(
            id=self._parse_id(data['id']),
            weight=data.get('weight', 1.0)
        )

    def _parse_id(self, id) -> int:
        return int(id, 16)
