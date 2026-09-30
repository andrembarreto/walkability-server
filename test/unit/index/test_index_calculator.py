from types import SimpleNamespace

from domain.index import distance
from domain.index.calculator import (
	group_events_by_segments,
	split_route_into_segments,
)
from domain.journey.event import Event

def make_position(identifier: int) -> SimpleNamespace:
	return SimpleNamespace(
		identifier=identifier,
		latitude=float(identifier),
		longitude=float(identifier),
	)


def make_event(identifier: int, position: SimpleNamespace) -> Event:
	return Event(id=identifier, position=position)


def test_split_route_into_segments_returns_empty_list_for_empty_route():
	assert split_route_into_segments([]) == []


def test_split_route_into_segments_returns_single_segment_when_route_fits(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2)]
	distances = iter([40, 60])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances),
	)

	assert split_route_into_segments(route) == [route]


def test_split_route_into_segments_splits_when_reference_length_is_exceeded(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2), make_position(3)]
	distances = iter([60, 50, 20])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances),
	)

	assert split_route_into_segments(route) == [
		[route[0], route[1]],
		[route[2], route[3]],
	]


def test_split_route_into_segments_does_not_split_at_exact_reference_length(
	monkeypatch,
):
	route = [make_position(0), make_position(1)]
	monkeypatch.setattr(distance, "calculate", lambda *args: 100)

	assert split_route_into_segments(route) == [route]


def test_split_route_into_segments_returns_single_position_as_one_segment():
	route = [make_position(0)]

	assert split_route_into_segments(route) == [route]


def test_group_events_by_segments_groups_events_by_their_route_segment(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2), make_position(3)]
	distances = iter([60, 50, 20])
	monkeypatch.setattr(
		distance,
		"calculate",
		lambda *args: next(distances),
	)
	events = [
		make_event(10, route[0]),
		make_event(11, route[1]),
		make_event(12, route[2]),
		make_event(13, route[3]),
	]

	assert group_events_by_segments(route, events) == [
		[events[0], events[1]],
		[events[2], events[3]],
	]


def test_group_events_by_segments_keeps_events_in_one_segment_at_100_meters(
	monkeypatch,
):
	route = [make_position(0), make_position(1), make_position(2)]
	monkeypatch.setattr(distance, "calculate", lambda *args: 50)
	events = [make_event(10, route[0]), make_event(11, route[2])]

	assert group_events_by_segments(route, events) == [events]


def test_group_events_by_segments_returns_empty_event_lists_when_route_has_no_events(
	monkeypatch,
):
	route = [make_position(0), make_position(1)]
	monkeypatch.setattr(distance, "calculate", lambda *args: 50)

	assert group_events_by_segments(route, []) == [[]]