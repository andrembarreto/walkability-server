import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

from dataclasses import dataclass

@dataclass(frozen=True)
class DBSession:
    client: MongoClient
    database_name: str

def get_session() -> DBSession:
    connection_string = os.getenv("MONGO_URI")
    client = MongoClient(connection_string)
    database_name = os.getenv("DATABASE_NAME")

    return DBSession(
        client=client,
        database_name=database_name
    )