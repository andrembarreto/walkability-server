from dataclasses import asdict

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