from dataclasses import dataclass

from domain.journey.position import Position
from domain.journey.event import Event

from . import index_table
from .index_table import EventInfluence

""" Usando um pouco mais de type hinting aqui para facilitar a compreensão """

@dataclass(frozen=True)
class IndexScore:
    global_score: float
    dimension_scores: dict[int, float]

def calculate_index_score(route: list[Position], events: list[Event]) -> IndexScore:
    events_by_segment: list[list[Event]] = group_events_by_segment(route=route, events=events)
    dimension_scores: dict[int, float] = {
        dimension_id: calculate_dimension_score(dimension_id, events_by_segment)
        for dimension_id in map(lambda d: d.id, index_table.get_dimensions())
    }
    global_score = sum(dimension_scores.values()) / len(dimension_scores)
    return IndexScore(global_score=global_score, dimension_scores=dimension_scores)

def group_events_by_segment(route: list[Position], events: list[Event]) -> list[list[Event]]:
    segments = split_route_into_segments(route)
    events_by_segment = []
    for segment in segments:
        events_in_segment = []
        for event in events:
            if event.position in segment:
                events_in_segment.append(event)
        events_by_segment.append(events_in_segment)
    return events_by_segment

def split_route_into_segments(route: list[Position]) -> list[list[Position]]:
    pass

def calculate_dimension_score(dimension_id: int, events_by_segment: list[list[Event]]) -> float:
    return sum([calculate_dimension_score_in_segment(dimension_id, segment_events) for segment_events in events_by_segment]) / len(events_by_segment)

def calculate_dimension_score_in_segment(dimension_id: int, segment_events: list[Event]) -> float:
    dimension = index_table.find_dimension(dimension_id)
    sum_of_scores = 0.0
    sum_of_weights = 0.0
    for criterium in dimension.criteria:
        criterium_events_in_segment = [index_table.find_event(event.id) for event in segment_events if index_table.find_event(event.id) in criterium.events]
        criterium_score_in_segment = calculate_criterium_score_in_segment(criterium_events_in_segment) * criterium.weight
        sum_of_scores += criterium_score_in_segment
        sum_of_weights += criterium.weight

    if sum_of_weights == 0:
        return 0.0

    return sum_of_scores / sum_of_weights

def calculate_criterium_score_in_segment(criterium_events: list[index_table.EventItem]) -> float:
    sum_of_positive_scores = 0.0
    sum_of_negative_scores = 0.0
    for event in criterium_events:
        count = criterium_events.count(event)
        if event.influence is EventInfluence.POSITIVE:
            sum_of_positive_scores += event.weight * count
        elif event.influence is EventInfluence.NEGATIVE:
            sum_of_negative_scores += event.weight * count

    return min(5, max(1, 3 + sum_of_positive_scores - sum_of_negative_scores))