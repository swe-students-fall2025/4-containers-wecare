import os
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

# Load environment variables from .env 
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# Database connection
MONGODB_CONNECTION = os.getenv("DATABASE_CONNECTION")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGODB_CONNECTION, server_api=ServerApi("1"))
client.admin.command("ping")

db = client.get_database(DB_NAME)


# Audio requests (what seniors say into the chatbot)
class audio_requests_dal:
    def insert_one_request(request_data: Dict[str, Any]) -> str:
        try:
            result = db.audio_requests.insert_one(request_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error inserting audio request: {e}")
            return ""

    def insert_many_requests(requests_data: List[Dict[str, Any]]) -> List[str]:
        try:
            result = db.audio_requests.insert_many(requests_data)
            return [str(_id) for _id in result.inserted_ids]
        except PyMongoError as e:
            print(f"Error inserting audio requests: {e}")
            return []

    def find_one_request(filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            request = db.audio_requests.find_one(filter)
            return request
        except PyMongoError as e:
            print(f"Error finding audio request: {e}")
            return None

    def find_many_requests(filter: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            requests = list(db.audio_requests.find(filter))
            return requests
        except PyMongoError as e:
            print(f"Error finding audio requests: {e}")
            return []

    def update_one_request(filter: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        try:
            result = db.audio_requests.update_one(filter, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating audio request: {e}")
            return False

    def update_many_requests(filter: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        try:
                result = db.audio_requests.update_many(filter, {"$set": update_data})
                return result.modified_count
        except PyMongoError as e:
            print(f"Error updating audio requests: {e}")
            return 0

    def delete_one_request(filter: Dict[str, Any]) -> bool:
        try:
            result = db.audio_requests.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting audio request: {e}")
            return False

    def delete_many_requests(filter: Dict[str, Any]) -> int:
        try:
            result = db.audio_requests.delete_many(filter)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting audio requests: {e}")
            return 0


# Bot responses (step-by-step instructions chatbot returns)
class bot_responses_dal:
    def insert_one_response(response_data: Dict[str, Any]) -> str:
        try:
            result = db.bot_responses.insert_one(response_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error inserting bot response: {e}")
            return ""

    def insert_many_responses(responses_data: List[Dict[str, Any]]) -> List[str]:
        try:
            result = db.bot_responses.insert_many(responses_data)
            return [str(_id) for _id in result.inserted_ids]
        except PyMongoError as e:
            print(f"Error inserting bot responses: {e}")
            return []

    def find_one_response(filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = db.bot_responses.find_one(filter)
            return response
        except PyMongoError as e:
            print(f"Error finding bot response: {e}")
            return None

    def find_many_responses(filter: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            responses = list(db.bot_responses.find(filter))
            return responses
        except PyMongoError as e:
            print(f"Error finding bot responses: {e}")
            return []

    def update_one_response(filter: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        try:
            result = db.bot_responses.update_one(filter, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating bot response: {e}")
            return False

    def update_many_responses(
        filter: Dict[str, Any], update_data: Dict[str, Any]
    ) -> int:
        try:
            result = db.bot_responses.update_many(filter, {"$set": update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"Error updating bot responses: {e}")
            return 0

    def delete_one_response(filter: Dict[str, Any]) -> bool:
        try:
            result = db.bot_responses.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting bot response: {e}")
            return False

    def delete_many_responses(filter: Dict[str, Any]) -> int:
        try:
            result = db.bot_responses.delete_many(filter)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting bot responses: {e}")
            return 0
