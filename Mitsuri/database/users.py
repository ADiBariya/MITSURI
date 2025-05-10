from pymongo import MongoClient
from datetime import datetime
from ..core.mongo import get_database


class UserModel:
    """
    Database model for managing user information.
    """

    def __init__(self):
        self.collection = get_database()["users"]

    def add_user(self, user_id: int, username: str):
        """
        Add or update a user in the database.
        :param user_id: Telegram user ID
        :param username: Telegram username
        """
        self.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "username": username,
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "joined_at": datetime.utcnow()
                }
            },
            upsert=True
        )

    def get_user(self, user_id: int):
        """
        Retrieve user data from the database.
        :param user_id: Telegram user ID
        :return: User document
        """
        return self.collection.find_one({"user_id": user_id})

    def delete_user(self, user_id: int):
        """
        Delete a user from the database.
        :param user_id: Telegram user ID
        """
        self.collection.delete_one({"user_id": user_id})

    def get_all_users(self):
        """
        Retrieve all users from the database.
        :return: List of user documents
        """
        return list(self.collection.find())
