from pymongo import MongoClient
from datetime import datetime
from ..core.mongo import get_database


class SettingsModel:
    """
    Database model for managing user and group settings.
    """

    def __init__(self):
        self.collection = get_database()["settings"]

    def update_user_settings(self, user_id: int, settings: dict):
        """
        Update settings for a specific user.
        :param user_id: Telegram user ID
        :param settings: Dictionary of settings to update
        """
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": settings, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )

    def update_group_settings(self, group_id: int, settings: dict):
        """
        Update settings for a specific group.
        :param group_id: Telegram group ID
        :param settings: Dictionary of settings to update
        """
        self.collection.update_one(
            {"group_id": group_id},
            {"$set": settings, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )

    def get_user_settings(self, user_id: int):
        """
        Retrieve settings for a specific user.
        :param user_id: Telegram user ID
        :return: Settings document
        """
        return self.collection.find_one({"user_id": user_id})

    def get_group_settings(self, group_id: int):
        """
        Retrieve settings for a specific group.
        :param group_id: Telegram group ID
        :return: Settings document
        """
        return self.collection.find_one({"group_id": group_id})
