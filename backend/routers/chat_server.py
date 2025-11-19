from flask import Blueprint, request, jsonify
from uuid import uuid4

from backend.DAL import chat_dal
chat_router = Blueprint('chats', __name__, url_prefix='/chats/api')

def ask_model(prompt: str) -> str:
    """Placeholder function so tests can monkeypatch it."""
    return "placeholder"

@chat_router.post('')
def create_chat():
    chat_data = request.json
    chat_data['_id'] = str(uuid4())
    inserted_id = chat_dal.insert_one_chat(chat_data)
    if inserted_id:
        return jsonify({"inserted_id": inserted_id}), 201
    return jsonify({"error": "Failed to create chat"}), 500

@chat_router.get('/<chat_id>')
def get_chat(chat_id):
    if not chat_id:
        return jsonify({"error": "chat_id query parameter is required"}), 400
    chat = chat_dal.find_one_chat({"_id": chat_id})
    if chat:
        return jsonify(chat), 200
    return jsonify({"error": "chat not found"}), 404

@chat_router.get('/')
def get_all_chats():
    chat = chat_dal.find_all_chats()
    if chat:
        return jsonify(chat), 200
    return jsonify({"error": "chats not found"}), 404


@chat_router.put('/<chat_id>')
def update_chat(chat_id):
    update_data = request.json
    success = chat_dal.update_one_chat({"_id": chat_id}, update_data)
    if success:
        return jsonify({"chat": "chat updated successfully"}), 200
    return jsonify({"error": "Failed to update chat"}), 500

@chat_router.delete('/<chat_id>')
def delete_chat(chat_id):
    success = chat_dal.delete_one_chat({"_id": chat_id})
    if success:
        return jsonify({"chat": "chat deleted successfully"}), 200
    return jsonify({"error": "Failed to delete chat"}), 500



@chat_router.post('/<chat_id>/message')
def send_message(chat_id):
    chat_data = request.json
    chat_data['_id'] = str(uuid4())
    inserted_id = chat_dal.insert_one_chat(chat_data)
    messages_for_model = [
        {"role": "user", "content": chat_data["content"]} #this is important because the way we structure the JS has to save message data as content
            
    ]
    assistant_reply = ask_model(messages_for_model)
    chat_data_2 = {
        "_id": str(uuid4()),
        "role": "assistant",
        "content": assistant_reply,
    }
    inserted_id_2 = chat_dal.insert_one_chat(chat_data_2)
    if inserted_id and inserted_id_2:
        return jsonify({"chat": "chat deleted successfully"}), 200
        
        
    return jsonify({"error": "Failed to create chat"}), 500




