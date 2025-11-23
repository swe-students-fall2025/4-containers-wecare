"""
Unit tests for messages_server.py
"""

import pytest
from backend.DAL import messages_dal
from backend.routers.messages_server import messages_router
from flask import Flask


# flask app fixture
@pytest.fixture
def test_client():
    """
    Create a test client for the messages server Flask app.
    """
    app = Flask(__name__)
    app.register_blueprint(messages_router)
    return app.test_client()


# test cases for messages_server.py
def test_create_message(test_client):  # pylint: disable=redefined-outer-name
    """
    Create a new message.
    """
    resp = test_client.post("/messages/api", json={"content": "hello"})
    assert resp.status_code == 201
    assert "inserted_id" in resp.get_json()


def test_get_message(test_client):  # pylint: disable=redefined-outer-name
    """
    get a specific message by ID.
    """
    msg_id = messages_dal.insert_one_message({"content": "test"})
    resp = test_client.get(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["content"] == "test"


def test_get_all_messages(test_client):  # pylint: disable=redefined-outer-name
    """
    get all messages.
    """
    messages_dal.insert_one_message({"a": 1})
    messages_dal.insert_one_message({"b": 2})
    resp = test_client.get("/messages/api/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_update_message(test_client):  # pylint: disable=redefined-outer-name
    """
    update a specific message by ID.
    """
    msg_id = messages_dal.insert_one_message({"x": 1})
    resp = test_client.put(f"/messages/api/{msg_id}", json={"x": 2})
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message updated successfully"


def test_delete_message(test_client):  # pylint: disable=redefined-outer-name
    """
    delete a specific message by ID.
    """
    msg_id = messages_dal.insert_one_message({"y": 3})
    resp = test_client.delete(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message deleted successfully"
