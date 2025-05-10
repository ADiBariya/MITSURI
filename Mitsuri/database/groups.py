from pymongo import MongoClient
from datetime import datetime
from ..core.mongo import get_database


class GroupModel:
    """
    Database model for managing group information.
    """

    def __init__(self):
        self.collection = get_database()["groups"]

    def add_group(self, group_id: int, title: str):
        """
        Add or update a group in the database.
        :param group_id: Telegram group ID
        :param title: Group title
        """
        self.collection.update_one(
            {"group_id": group_id},
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )

    def get_group(self, group_id: int):
        """
        Retrieve group data from the database.
        :param group_id: Telegram group ID
        :return: Group document
        """
        return self.collection.find_one({"group_id": group_id})

    def delete_group(self, group_id: int):
        """
        Delete a group from the database.
        :param group_id: Telegram group ID
        """
        self.collection.delete_one({"group_id": group_id})

    def get_all_groups(self):
        """
        Retrieve all groups from the database.
        :return: List of group documents
        """
        return list(self.collection.find())
