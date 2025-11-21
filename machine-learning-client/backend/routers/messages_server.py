from flask import Blueprint, request, jsonify
from uuid import uuid4

from backend.DAL import messages_dal

messages_router = Blueprint("messages", __name__, url_prefix="/messages/api")


@messages_router.post("")
def create_message():
    message_data = request.json
    message_data["_id"] = str(uuid4())
    inserted_id = messages_dal.insert_one_message(message_data)
    if inserted_id:
        return jsonify({"inserted_id": inserted_id}), 201
    return jsonify({"error": "Failed to create message"}), 500


@messages_router.get("/<message_id>")
def get_message(message_id):
    if not message_id:
        return jsonify({"error": "message_id query parameter is required"}), 400
    message = messages_dal.find_one_message({"_id": message_id})
    if message:
        return jsonify(message), 200
    return jsonify({"error": "Message not found"}), 404


@messages_router.get("/")
def get_all_messages():
    message = messages_dal.find_all_messages()
    if message:
        return jsonify(message), 200
    return jsonify({"error": "Messages not found"}), 404


@messages_router.put("/<message_id>")
def update_message(message_id):
    update_data = request.json
    success = messages_dal.update_one_message({"_id": message_id}, update_data)
    if success:
        return jsonify({"message": "Message updated successfully"}), 200
    return jsonify({"error": "Failed to update message"}), 500


@messages_router.delete("/<message_id>")
def delete_message(message_id):
    success = messages_dal.delete_one_message({"_id": message_id})
    if success:
        return jsonify({"message": "Message deleted successfully"}), 200
    return jsonify({"error": "Failed to delete Message"}), 500
