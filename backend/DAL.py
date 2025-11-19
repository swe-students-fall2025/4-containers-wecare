import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

# # Load environment variables from .env
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# MONGODB_CONNECTION = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("MONGO_DB")

# if not MONGODB_CONNECTION or not DB_NAME:
#     raise RuntimeError(
#         "DATABASE_CONNECTION and DB_NAME must be set in the .env file"
#     )

# # client = MongoClient(MONGODB_CONNECTION)
# # client.admin.command("ping")
# # db = client.get_database(DB_NAME)
# if DATABASE_CONNECTION == "mock":
#     db = None
# else:
#     client = MongoClient(DATABASE_CONNECTION)
#     client.admin.command("ping")
#     db = client[DB_NAME]


DATABASE_CONNECTION = os.getenv("DATABASE_CONNECTION")
DB_NAME = os.getenv("DB_NAME")

# 🟢 During tests, conftest.py sets DATABASE_CONNECTION = "mock"
# so we skip real DB setup entirely
if DATABASE_CONNECTION == "mock":
    db = None

else:
    # Normal runtime: still require env vars
    if not DATABASE_CONNECTION or not DB_NAME:
        raise RuntimeError(
            "DATABASE_CONNECTION and DB_NAME must be set in the .env file"
        )

    # Try DB setup
    client = MongoClient(DATABASE_CONNECTION, serverSelectionTimeoutMS=1000)

    try:
        client.admin.command("ping")
    except Exception as e:
        raise RuntimeError(f"Could not connect to MongoDB: {e}")

    db = client[DB_NAME]


# Chats: one document per conversation
class chat_dal:
    @staticmethod
    def insert_one_chat(chat_data: Dict[str, Any]) -> str:
        try:
            result = db.chats.insert_one(chat_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error inserting chat: {e}")
            return ""

    @staticmethod
    def find_one_chat(filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return db.chats.find_one(filter)
        except PyMongoError as e:
            print(f"Error finding chat: {e}")
            return None

    @staticmethod
    def find_all_chats() -> List[Dict[str, Any]]:
        try:
            return list(db.chats.find({}))
        except PyMongoError as e:
            print(f"Error finding chats: {e}")
            return []

    @staticmethod
    def update_one_chat(
        filter: Dict[str, Any], update_data: Dict[str, Any]
    ) -> bool:
        try:
            result = db.chats.update_one(filter, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating chat: {e}")
            return False

    @staticmethod
    def delete_one_chat(filter: Dict[str, Any]) -> bool:
        try:
            result = db.chats.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting chat: {e}")
            return False


# Messages: one document per message in a chat
# can store audio URL, transcript, sender, bot answer, etc
class messages_dal:
    @staticmethod
    def insert_one_message(message_data: Dict[str, Any]) -> str:
        try:
            result = db.messages.insert_one(message_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error inserting message: {e}")
            return ""

    @staticmethod
    def find_one_message(filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return db.messages.find_one(filter)
        except PyMongoError as e:
            print(f"Error finding message: {e}")
            return None

    @staticmethod
    def find_all_messages() -> List[Dict[str, Any]]:
        try:
            return list(db.messages.find({}))
        except PyMongoError as e:
            print(f"Error finding messages: {e}")
            return []

    @staticmethod
    def update_one_message(
        filter: Dict[str, Any], update_data: Dict[str, Any]
    ) -> bool:
        try:
            result = db.messages.update_one(filter, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating message: {e}")
            return False

    @staticmethod
    def delete_one_message(filter: Dict[str, Any]) -> bool:
        try:
            result = db.messages.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting message: {e}")
            return False
