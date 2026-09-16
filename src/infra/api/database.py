import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

class DBConnection:
    _client: MongoClient = None
    _database: Database = None

    @staticmethod
    def get_session() -> Database:
        if DBConnection._database is not None:
            return DBConnection._database

        connection_string = os.getenv("MONGO_URI")
        database_name = os.getenv("DATABASE_NAME")

        try:
            client = MongoClient(connection_string, uuidRepresentation='standard')
            client.admin.command('ping')
            DBConnection._client = client
            DBConnection._database = client[database_name]

            return DBConnection._database
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e