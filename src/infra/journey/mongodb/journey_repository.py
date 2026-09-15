from src.domain.journey.journey_repository_interface import JourneyRepositoryInterface

class JourneyRepository(JourneyRepositoryInterface):
    def __init__(self, connection_string: str = "mongodb://localhost:27017", database_name: str = "journey_db"):
        pass

    def save(self, journey):
        raise NotImplementedError("The save method is not implemented yet.")