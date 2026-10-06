from typing import Callable

from domain.journey.position import Position

from . import distance

SEGMENT_REFERENCE_LENGTH_METERS = 100

RouteSplitter = Callable[[list[Position]], list[list[Position]]]


def split_by_accumulated_length(route: list[Position]) -> list[list[Position]]:
    if len(route) == 0:
        return []

    p1_index = 0
    p2_index = 1
    current_segment = [route[p1_index]]
    current_segment_tentative_length = 0
    segments = []

    while len(route) > p2_index:
        p1 = route[p1_index]
        p2 = route[p2_index]
        points_distance = distance.calculate(
            p1.latitude, p1.longitude, p2.latitude, p2.longitude
        )
        current_segment_tentative_length += points_distance
        if current_segment_tentative_length > SEGMENT_REFERENCE_LENGTH_METERS:
            segments.append(current_segment)
            current_segment_tentative_length = 0
            current_segment = []
        current_segment.append(p2)
        p1_index += 1
        p2_index += 1

    if len(current_segment) > 0:
        segments.append(current_segment)

    return segments


def split_by_distance_from_head(route: list[Position]) -> list[list[Position]]:
    if len(route) == 0:
        return []

    segment_head = route[0]
    current_segment = [segment_head]
    segments = []

    for position in route[1:]:
        distance_from_head = distance.calculate(
            segment_head.latitude, segment_head.longitude,
            position.latitude, position.longitude
        )
        if distance_from_head >= SEGMENT_REFERENCE_LENGTH_METERS:
            segments.append(current_segment)
            segment_head = position
            current_segment = []
        current_segment.append(position)

    segments.append(current_segment)

    return segments
