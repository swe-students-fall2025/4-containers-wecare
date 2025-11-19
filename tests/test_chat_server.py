import pytest
from flask import Flask
from backend.routers.chat_server import chat_router

#flask app fixture
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(chat_router)
    return app.test_client()

#test cases for chat_server.py
def test_create_chat(client):
    resp = client.post("/chats/api", json={"text": "hello"})
    assert resp.status_code == 201
    assert "inserted_id" in resp.get_json()

def test_get_chat(client):
    resp = client.get("/chats/api/123")
    assert resp.status_code == 200
    assert resp.get_json()["_id"] == "123"

def test_get_all_chats(client):
    resp = client.get("/chats/api/")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_update_chat(client):
    resp = client.put("/chats/api/123", json={"text": "updated"})
    assert resp.status_code == 200
    assert resp.get_json()["chat"] == "chat updated successfully"

def test_delete_chat(client):
    resp = client.delete("/chats/api/123")
    assert resp.status_code == 200
    assert resp.get_json()["chat"] == "chat deleted successfully"

def test_send_message(client):
    resp = client.post("/chats/api/123/message", json={"content": "hi"})
    assert resp.status_code == 200
    assert resp.get_json()["assistant_response"] == "assistant reply"
