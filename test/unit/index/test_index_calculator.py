from types import SimpleNamespace

from domain.index import distance
from domain.index.calculator import Calculator, group_events_by_segments
from domain.index.segmentation import (
	split_by_accumulated_length,
	split_by_distance_from_head,
)
from domain.index.table import CriteriumItem, DimensionItem, EventItem
from domain.journey.event import Event

def make_position(identifier: int) -> SimpleNamespace:
	return SimpleNamespace(
		identifier=identifier,
		latitude=float(identifier),
		longitude=float(identifier),
	)


def make_event(identifier: int, position: SimpleNamespace) -> Event:
	return Event(id=identifier, position=position)


def test_split_by_accumulated_length_returns_empty_list_for_empty_route():
	assert split_by_accumulated_length([]) == []


def test_split_by_accumulated_length_returns_single_segment_when_route_fits(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2)]
	distances = iter([40, 60])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances),
	)

	assert split_by_accumulated_length(route) == [route]


def test_split_by_accumulated_length_splits_when_reference_length_is_exceeded(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2), make_position(3)]
	distances = iter([60, 50, 20])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances),
	)

	assert split_by_accumulated_length(route) == [
		[route[0], route[1]],
		[route[2], route[3]],
	]


def test_split_by_accumulated_length_does_not_split_at_exact_reference_length(
	monkeypatch,
):
	route = [make_position(0), make_position(1)]
	monkeypatch.setattr(distance, "calculate", lambda *args: 100)

	assert split_by_accumulated_length(route) == [route]


def test_split_by_accumulated_length_returns_single_position_as_one_segment():
	route = [make_position(0)]

	assert split_by_accumulated_length(route) == [route]


def test_split_by_distance_from_head_returns_empty_list_for_empty_route():
	assert split_by_distance_from_head([]) == []


def test_split_by_distance_from_head_returns_single_position_as_one_segment():
	route = [make_position(0)]

	assert split_by_distance_from_head(route) == [route]


def test_split_by_distance_from_head_keeps_positions_closer_than_reference_together(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2)]
	distances_from_head = iter([60, 99])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances_from_head),
	)

	assert split_by_distance_from_head(route) == [route]


def test_split_by_distance_from_head_measures_from_head_not_from_previous_position(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2), make_position(3)]
	distances_from_head = {(0, 1): 60, (0, 2): 120, (2, 3): 30}
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda lat1, lon1, lat2, lon2: distances_from_head[(int(lat1), int(lat2))],
	)

	assert split_by_distance_from_head(route) == [
		[route[0], route[1]],
		[route[2], route[3]],
	]


def test_split_by_distance_from_head_splits_at_exact_reference_length(
	monkeypatch,
):
	route = [make_position(0), make_position(1)]
	monkeypatch.setattr(distance, "calculate", lambda *args: 100)

	assert split_by_distance_from_head(route) == [[route[0]], [route[1]]]


def test_group_events_by_segments_groups_events_by_their_route_segment():
	route = [make_position(0), make_position(1), make_position(2), make_position(3)]
	segments = [[route[0], route[1]], [route[2], route[3]]]
	events = [
		make_event(10, route[0]),
		make_event(11, route[1]),
		make_event(12, route[2]),
		make_event(13, route[3]),
	]

	assert group_events_by_segments(segments, events) == [
		[events[0], events[1]],
		[events[2], events[3]],
	]


def test_group_events_by_segments_groups_events_from_non_contiguous_positions():
	route = [make_position(0), make_position(1), make_position(2)]
	segments = [[route[0], route[2]], [route[1]]]
	events = [make_event(10, route[0]), make_event(11, route[2])]

	assert group_events_by_segments(segments, events) == [events, []]


def test_group_events_by_segments_returns_empty_event_lists_when_route_has_no_events():
	route = [make_position(0), make_position(1)]

	assert group_events_by_segments([route], []) == [[]]


def test_calculator_scores_the_segments_returned_by_the_injected_splitter():
	table = SimpleNamespace(
		dimensions=[
			DimensionItem(
				id=1,
				name="Segurança",
				criteria=[
					CriteriumItem(
						id=1,
						name="Iluminação",
						weight=1.0,
						events=[EventItem(id=10, name="Sem iluminação", weight=1.0)],
					)
				],
			)
		],
	)
	table.find_dimension = lambda dimension_id: table.dimensions[0]
	table.find_event = lambda event_id: table.dimensions[0].criteria[0].events[0]
	route = [make_position(0), make_position(1), make_position(2)]
	events = [make_event(10, route[0])]
	calculator = Calculator(table, split_route=lambda route: [[route[0]], [route[1], route[2]]])

	score = calculator.calculate(route, events)

	assert score.dimension_scores == {1: 5.0}
