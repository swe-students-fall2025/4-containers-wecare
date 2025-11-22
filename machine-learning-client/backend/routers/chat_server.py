from datetime import datetime
from uuid import uuid4

from backend.DAL import chat_dal
from backend.routers.model_client import ask_model
from flask import Blueprint, jsonify, request

chat_router = Blueprint("chats", __name__, url_prefix="/chats/api")


@chat_router.post("")
def create_chat():
    chat_data = request.json
    chat_data["_id"] = str(uuid4())
    inserted_id = chat_dal.insert_one_chat(chat_data)
    if inserted_id:
        return jsonify({"inserted_id": inserted_id}), 201
    return jsonify({"error": "Failed to create chat"}), 500


@chat_router.get("/<chat_id>")
def get_chat(chat_id):
    if not chat_id:
        return jsonify({"error": "chat_id query parameter is required"}), 400
    chat = chat_dal.find_one_chat({"_id": chat_id})
    if chat:
        return jsonify(chat), 200
    return jsonify({"error": "chat not found"}), 404


@chat_router.get("/")
def get_all_chats():
    chat = chat_dal.find_all_chats()
    if chat:
        return jsonify(chat), 200
    return jsonify({"error": "chats not found"}), 404


@chat_router.put("/<chat_id>")
def update_chat(chat_id):
    update_data = request.json
    success = chat_dal.update_one_chat({"_id": chat_id}, update_data)
    if success:
        return jsonify({"chat": "chat updated successfully"}), 200
    return jsonify({"error": "Failed to update chat"}), 500


@chat_router.delete("/<chat_id>")
def delete_chat(chat_id):
    success = chat_dal.delete_one_chat({"_id": chat_id})
    if success:
        return jsonify({"chat": "chat deleted successfully"}), 200
    return jsonify({"error": "Failed to delete chat"}), 500


@chat_router.post("/<chat_id>/message")
def send_message(chat_id):

    chat = chat_dal.find_one_chat({"_id": chat_id})
    if not chat:
        return jsonify({"error": "chat not found"}), 404

    usr_message = request.json
    usr_message["_id"] = str(uuid4())
    usr_message["timestamp"] = datetime.now().isoformat()

    messages = chat.get("messages", [])
    messages.append(usr_message)

    # get ai response
    ai_reply = ask_model(messages)
    ai_message = {
        "_id": str(uuid4()),
        "role": "assistant",
        "content": ai_reply,
        "timestamp": datetime.now().isoformat(),
    }
    messages.append(ai_message)

    # update chat with new messages
    success = chat_dal.update_one_chat({"_id": chat_id}, {"messages": messages})

    if success:
        return jsonify(ai_message), 200

    return jsonify({"error": "Failed to send message"}), 500
