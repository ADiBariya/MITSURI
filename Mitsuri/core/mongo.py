import logging
from pymongo import MongoClient, errors
from ..config import Config

logger = logging.getLogger("Mitsuri.core.mongo")


class MongoDB:
    """
    MongoDB Connector for Mitsuri Bot.
    Provides a singleton connection to the database and utility methods.
    """

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish connection to the MongoDB database.
        """
        try:
            logger.info("Connecting to MongoDB...")
            self.client = MongoClient(Config.DATABASE_URI, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Trigger connection test
            self.db = self.client["mitsuri_db"]  # Database name
            logger.info("MongoDB connection established.")
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise ConnectionError("Could not connect to MongoDB.")

    def get_collection(self, name: str):
        """
        Retrieve a specific collection from the database.
        :param name: Collection name
        :return: MongoDB Collection object
        """
        if not self.db:
            raise ConnectionError("No active MongoDB connection.")
        return self.db[name]

    def close(self):
        """
        Safely close the MongoDB connection.
        """
        if self.client:
            logger.info("Closing MongoDB connection...")
            self.client.close()
            logger.info("MongoDB connection closed.")


# Singleton instance of MongoDB
mongodb = MongoDB()
mongodb.connect()
