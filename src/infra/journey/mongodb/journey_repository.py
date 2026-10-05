from dataclasses import asdict
import logging
from uuid import UUID

from pymongo.database import Database
from pymongo.errors import PyMongoError

from domain.journey.journey import Journey
from domain.journey.journey_repository_interface import JourneyRepositoryInterface
from domain.journey.event import Event
from domain.journey.position import Position

logger = logging.getLogger(__name__)

class JourneyRepository(JourneyRepositoryInterface):
    def __init__(self, session: Database):
        self.__collection = session["journeys"]

    def save(self, journey: Journey) -> Journey:
        try:
            self.__collection.insert_one(self._encode_journey(journey))
            return journey
        except PyMongoError:
            logger.exception("Erro ao salvar jornada no MongoDB")
            return None

    def find(self, journey_id: UUID) -> Journey:
        try:
            journey_data = self.__collection.find_one({"_id": str(journey_id)})
            if journey_data:
                return self._parse_journey(journey_data)
            else:
                return None
        except PyMongoError:
            logger.exception("Erro ao buscar jornada no MongoDB")
            return None

    def find_all(self) -> list[Journey]:
        try:
            return [self._parse_journey(data) for data in self.__collection.find()]
        except PyMongoError:
            logger.exception("Erro ao listar jornadas no MongoDB")
            return []

    def _encode_journey(self, journey: Journey) -> dict:
        return {
            "_id": str(journey.id),
            "route": [asdict(position) for position in journey.route],
            "events": [
                {
                    "id": event.id,
                    "position": asdict(event.position),
                }
                for event in journey.events
            ],
        }

    def _parse_journey(self, data: dict) -> Journey:
        return Journey(
            id=UUID(str(data["_id"])),
            route=[
                Position(
                    latitude=position["latitude"],
                    longitude=position["longitude"],
                    timestamp=position["timestamp"],
                )
                for position in data["route"]
            ],
            events=[
                Event(
                    id=event["id"],
                    position=Position(
                        latitude=event["position"]["latitude"],
                        longitude=event["position"]["longitude"],
                        timestamp=event["position"]["timestamp"],
                    ),
                )
                for event in data["events"]
            ],
        )