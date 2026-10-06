from dataclasses import dataclass

from domain.journey.position import Position
from domain.journey.event import Event

from .table import Table, EventItem
from .segmentation import RouteSplitter

MAX_SCORE = 10.0

@dataclass(frozen=True)
class Score:
    global_score: float
    dimension_scores: dict[int, float]


def group_events_by_segments(
    segments: list[list[Position]], events: list[Event]
) -> list[list[Event]]:
    events_by_segment = []
    for segment in segments:
        events_in_segment = []
        for event in events:
            if event.position in segment:
                events_in_segment.append(event)
        events_by_segment.append(events_in_segment)
    return events_by_segment


class Calculator:
    def __init__(self, table: Table, split_route: RouteSplitter):
        self._table = table
        self._split_route = split_route

    def calculate(self, route: list[Position], events: list[Event]) -> Score:
        events_by_segments: list[list[Event]] = group_events_by_segments(
            segments=self._split_route(route), events=events
        )
        dimension_scores: dict[int, float] = {
            dimension.id: self.calculate_dimension_final_score(dimension.id, events_by_segments)
            for dimension in self._table.dimensions
        }
        global_score = sum(dimension_scores.values()) / len(dimension_scores) if dimension_scores else 0.0
        return Score(global_score=global_score, dimension_scores=dimension_scores)

    def calculate_dimension_final_score(self, dimension_id: int, events_by_segments: list[list[Event]]) -> float:
        if not events_by_segments:
            return 0.0
        return sum([self.calculate_dimension_score_in_segment(dimension_id, segment_events) for segment_events in events_by_segments]) \
            / len(events_by_segments)

    def calculate_dimension_score_in_segment(self, dimension_id: int, segment_events: list[Event]) -> float:
        dimension = self._table.find_dimension(dimension_id)
        sum_of_scores = 0.0
        sum_of_weights = 0.0
        for criterium in dimension.criteria:
            criterium_events_in_segment = [self._table.find_event(event.id) for event in segment_events if self._table.find_event(event.id) in criterium.events]
            criterium_score_in_segment = self.calculate_criterium_score_in_segment(criterium_events_in_segment) * criterium.weight
            sum_of_scores += criterium_score_in_segment
            sum_of_weights += criterium.weight

        if sum_of_weights == 0:
            return 0.0

        return sum_of_scores / sum_of_weights

    def calculate_criterium_score_in_segment(self, criterium_events: list[EventItem]) -> float:
        penalty = 0
        for event in criterium_events:
            occurrences = criterium_events.count(event)
            penalty += MAX_SCORE * event.weight * occurrences

        return max(0, MAX_SCORE - penalty)