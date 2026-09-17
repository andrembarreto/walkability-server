from dataclasses import asdict
from uuid import UUID

from pymongo.database import Database
from pymongo.errors import PyMongoError


from domain.journey.journey import Journey
from domain.journey.journey_repository_interface import JourneyRepositoryInterface

class JourneyRepository(JourneyRepositoryInterface):
    def __init__(self, session: Database):
        self.__collection = session["journeys"]

    def save(self, journey: Journey) -> Journey:
        try:
            self.__collection.insert_one(asdict(journey))
            return journey
        except PyMongoError as e:
            print(f"Error saving journey: {e}")
            return None

    def find(self, journey_id: UUID) -> Journey:
        try:
            journey_data = self.__collection.find_one({"id": str(journey_id)})
            if journey_data:
                return Journey(**journey_data)
            else:
                return None
        except PyMongoError as e:
            print(f"Error finding journey: {e}")
            return None