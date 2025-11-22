"""
Tests for chat_server.py
"""

import pytest
from backend.routers.chat_server import chat_router
from flask import Flask


# flask app fixture
@pytest.fixture
def client():
    """
    Create a test client for the chat server Flask app.
    """
    app = Flask(__name__)
    app.register_blueprint(chat_router)
    return app.test_client()


# test cases for chat_server.py
def test_create_chat(client):
    """
    Create a new chat.
    """
    resp = client.post("/chats/api", json={"text": "hello"})
    assert resp.status_code == 201
    assert "inserted_id" in resp.get_json()


def test_get_chat(client):
    """
    Get a specific chat by ID.
    """
    resp = client.get("/chats/api/123")
    assert resp.status_code == 200
    assert resp.get_json()["_id"] == "123"


def test_get_all_chats(client):
    """
    get all chats.
    """
    resp = client.get("/chats/api/")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_update_chat(client):
    """
    update a specific chat by ID.
    """
    resp = client.put("/chats/api/123", json={"text": "updated"})
    assert resp.status_code == 200
    assert resp.get_json()["chat"] == "chat updated successfully"


def test_delete_chat(client):
    """
    delete a specific chat by ID.
    """
    resp = client.delete("/chats/api/123")
    assert resp.status_code == 200
    assert resp.get_json()["chat"] == "chat deleted successfully"


def test_send_message(client):
    """
    send a message to a specific chat.
    """
    resp = client.post("/chats/api/123/message", json={"content": "hi"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["role"] == "assistant"
    assert data["content"] == "assistant reply"
    assert "timestamp" in data
