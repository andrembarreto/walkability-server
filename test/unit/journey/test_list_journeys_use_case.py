from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from application.list_journeys.list_journeys_use_case import ListJourneysUseCase
from domain.journey.journey import Journey
from domain.journey.position import Position


def make_position(timestamp):
    return Position(latitude=-23.5505, longitude=-46.6333, timestamp=timestamp)

def make_journey(timestamps):
    return Journey(id=uuid4(), route=[make_position(t) for t in timestamps], events=[])

def make_use_case(journeys):
    repository = MagicMock()
    repository.find_all.return_value = journeys
    return ListJourneysUseCase(journey_repository=repository)

def test_summary_has_start_and_duration():
    journey = make_journey([datetime(2026, 1, 1, 12, 0, 0), datetime(2026, 1, 1, 12, 30, 34)])

    output = make_use_case([journey]).execute()

    assert len(output.journeys) == 1
    assert output.journeys[0].journey_id == journey.id
    assert output.journeys[0].started_at == datetime(2026, 1, 1, 12, 0, 0)
    assert output.journeys[0].duration == "00:30:34"

def test_duration_over_24_hours():
    journey = make_journey([datetime(2026, 1, 1, 12, 0, 0), datetime(2026, 1, 2, 13, 0, 0)])

    output = make_use_case([journey]).execute()

    assert output.journeys[0].duration == "25:00:00"

def test_single_point_route_has_zero_duration():
    journey = make_journey([datetime(2026, 1, 1, 12, 0, 0)])

    output = make_use_case([journey]).execute()

    assert output.journeys[0].duration == "00:00:00"

def test_empty_route_is_ignored():
    output = make_use_case([make_journey([])]).execute()

    assert output.journeys == []

def test_no_journeys_returns_empty_list():
    output = make_use_case([]).execute()

    assert output.journeys == []

def test_sorted_by_started_at_descending():
    older = make_journey([datetime(2026, 1, 1, 8, 0, 0)])
    newer = make_journey([datetime(2026, 1, 3, 8, 0, 0)])
    middle = make_journey([datetime(2026, 1, 2, 8, 0, 0)])

    output = make_use_case([older, newer, middle]).execute()

    assert [j.journey_id for j in output.journeys] == [newer.id, middle.id, older.id]
