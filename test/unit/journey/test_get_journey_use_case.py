import json
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.get_journey.get_journey_dtos import GetJourneyInputDTO
from application.get_journey.get_journey_use_case import GetJourneyUseCase
from domain.index.table import Table
from domain.journey.event import Event
from domain.journey.journey import Journey
from domain.journey.position import Position


def make_table(tmp_path):
    source = tmp_path / "table.json"
    source.write_text(json.dumps({
        "dimensions": [{
            "id": "0x00",
            "name": "Segurança",
            "criteria": [{
                "id": "0x00000",
                "name": "Taxa de criminalidade da região",
                "weight": 1.0,
                "events": [
                    {"id": "0x00000000", "name": "Segmento totalmente deserto", "weight": 1.0},
                    {"id": "0x00000001", "name": "Segmento superlotado", "weight": 0.5},
                ],
            }],
        }]
    }))
    return Table(source=str(source))

def make_journey(event_ids):
    position = Position(
        latitude=-23.5505,
        longitude=-46.6333,
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
    )
    return Journey(
        id=uuid4(),
        route=[position],
        events=[Event(id=event_id, position=position) for event_id in event_ids],
    )

def make_use_case(tmp_path, journey):
    repository = MagicMock()
    repository.find.return_value = journey
    return GetJourneyUseCase(journey_repository=repository, index_table=make_table(tmp_path))

def test_maps_route_and_events_with_description(tmp_path):
    journey = make_journey([0, 1])
    use_case = make_use_case(tmp_path, journey)

    output = use_case.execute(GetJourneyInputDTO(journey_id=str(journey.id)))

    assert output.journey_id == journey.id
    assert len(output.route) == 1
    assert output.route[0].lat == -23.5505
    assert output.route[0].long == -46.6333
    assert output.route[0].time == datetime(2026, 1, 1, 12, 0, 0)
    assert [(e.id, e.description) for e in output.events] == [
        (0, "Segmento totalmente deserto"),
        (1, "Segmento superlotado"),
    ]
    assert output.events[0].pos.lat == -23.5505
    assert output.events[0].pos.long == -46.6333

def test_unknown_event_gets_fallback_description(tmp_path):
    journey = make_journey([999])
    use_case = make_use_case(tmp_path, journey)

    output = use_case.execute(GetJourneyInputDTO(journey_id=str(journey.id)))

    assert output.events[0].description == "Evento 999"

def test_journey_not_found_raises_value_error(tmp_path):
    use_case = make_use_case(tmp_path, None)

    with pytest.raises(ValueError):
        use_case.execute(GetJourneyInputDTO(journey_id="inexistente"))
