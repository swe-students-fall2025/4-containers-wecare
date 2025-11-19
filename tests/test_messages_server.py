import pytest
from backend.routers.messages_server import messages_router
from backend.DAL import messages_dal
from flask import Flask
from unittest.mock import MagicMock


# mock database collections
class FakeCollection:
    def __init__(self):
        self.storage = {}
        self.counter = 0

    def insert_one(self, data):
        self.counter += 1
        _id = str(self.counter)
        self.storage[_id] = data
        return MagicMock(inserted_id=_id)

    def find_one(self, filter):
        for _id, data in self.storage.items():
            if all(item in data.items() for item in filter.items()):
                return data
        return None

    def find(self, _):
        return list(self.storage.values())

    def update_one(self, filter, update_data):
        modified = 0
        for _id, data in self.storage.items():
            if all(item in data.items() for item in filter.items()):
                data.update(update_data["$set"])
                modified = 1
        return MagicMock(modified_count=modified)

    def delete_one(self, filter):
        deleted = 0
        to_delete = None
        for _id, data in self.storage.items():
            if all(item in data.items() for item in filter.items()):
                to_delete = _id
                deleted = 1
        if to_delete:
            del self.storage[to_delete]
        return MagicMock(deleted_count=deleted)


class FakeDB:
    def __init__(self):
        self.messages = FakeCollection()


# pytest fixture to mock db in DAL.py
@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    fake = FakeDB()
    monkeypatch.setattr("backend.DAL.db", fake)
    return fake

# Flask app fixture with messages router
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(messages_router)
    return app.test_client()



# messages server tests
def test_create_message(client):
    resp = client.post("/messages/api", json={"content": "hello"})
    assert resp.status_code == 201
    assert "inserted_id" in resp.get_json()


def test_get_message(client, mock_db):
    # prepare fake message
    msg_id = messages_dal.insert_one_message({"content": "test"})
    resp = client.get(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["content"] == "test"


def test_get_all_messages(client, mock_db):
    messages_dal.insert_one_message({"a": 1})
    messages_dal.insert_one_message({"b": 2})
    resp = client.get("/messages/api/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_update_message(client, mock_db):
    msg_id = messages_dal.insert_one_message({"x": 1})
    resp = client.put(f"/messages/api/{msg_id}", json={"x": 2})
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message updated successfully"


def test_delete_message(client, mock_db):
    msg_id = messages_dal.insert_one_message({"y": 3})
    resp = client.delete(f"/messages/api/{msg_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Message deleted successfully"
