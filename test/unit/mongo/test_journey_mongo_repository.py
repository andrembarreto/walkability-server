from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from domain.journey.event import Event
from domain.journey.journey import Journey
from domain.journey.position import Position
from infra.journey.mongodb.journey_repository import JourneyRepository


def make_journey():
    position = Position(
        latitude=-23.5505,
        longitude=-46.6333,
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
    )
    return Journey(
        id=uuid4(),
        route=[position],
        events=[Event(id=1, position=position)],
    )

def test_encode_journey_to_mongo_document():
    repository = JourneyRepository(MagicMock())
    journey = make_journey()

    document = repository._encode_journey(journey)

    assert document == {
        "_id": str(journey.id),
        "route": [
            {
                "latitude": -23.5505,
                "longitude": -46.6333,
                "timestamp": datetime(2026, 1, 1, 12, 0, 0),
            }
        ],
        "events": [
            {
                "id": 1,
                "position": {
                    "latitude": -23.5505,
                    "longitude": -46.6333,
                    "timestamp": datetime(2026, 1, 1, 12, 0, 0),
                },
            }
        ],
    }

def test_parse_mongo_document_to_journey():
    repository = JourneyRepository(MagicMock())
    journey = make_journey()

    parsed_journey = repository._parse_journey(repository._encode_journey(journey))

    assert parsed_journey == journey

def test_find_all_returns_parsed_journeys():
    session = MagicMock()
    repository = JourneyRepository(session)
    journey = make_journey()
    session["journeys"].find.return_value = [repository._encode_journey(journey)]

    assert repository.find_all() == [journey]
