import pytest
from flask import Flask
from backend.routers.messages_server import messages_router
from backend.DAL import messages_dal

#flask app fixture
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(messages_router)
    return app.test_client()

#test cases for messages_server.py
def test_create_message(client):
    resp = client.post("/messages/api", json={"content": "hello"})
    assert resp.status_code == 201
    assert "inserted_id" in resp.get_json()

def test_get_message(client):
    msg_id = messages_dal.insert_one_message({"content": "test"})
    resp = client.get(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["content"] == "test"

def test_get_all_messages(client):
    messages_dal.insert_one_message({"a": 1})
    messages_dal.insert_one_message({"b": 2})
    resp = client.get("/messages/api/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2

def test_update_message(client):
    msg_id = messages_dal.insert_one_message({"x": 1})
    resp = client.put(f"/messages/api/{msg_id}", json={"x": 2})
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message updated successfully"

def test_delete_message(client):
    msg_id = messages_dal.insert_one_message({"y": 3})
    resp = client.delete(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message deleted successfully"
