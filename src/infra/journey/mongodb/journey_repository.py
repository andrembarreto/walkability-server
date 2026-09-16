from pymongo import MongoClient

from domain.journey.journey_repository_interface import JourneyRepositoryInterface

class JourneyRepository(JourneyRepositoryInterface):
    def __init__(self, client: MongoClient, database_name: str):
        pass

    def save(self, journey):
        raise NotImplementedError("The save method is not implemented yet.")