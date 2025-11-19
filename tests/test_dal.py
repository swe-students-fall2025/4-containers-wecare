import pytest
from unittest.mock import MagicMock
from backend.DAL import chat_dal, messages_dal


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

    def find(self, filter):
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
        self.chats = FakeCollection()
        self.messages = FakeCollection()


# pytest fixture to mock db in DAL.py
@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr("backend.DAL.db", fake_db)
    return fake_db

#chats tests
def test_chat_insert_one():
    chat_id = chat_dal.insert_one_chat({"user": "amy", "text": "hello"})
    assert chat_id != ""

def test_chat_find_one(mock_db):
    chat_dal.insert_one_chat({"user": "amy", "text": "msg"})
    result = chat_dal.find_one_chat({"user": "amy"})
    assert result is not None
    assert result["user"] == "amy"

def test_chat_find_all(mock_db):
    chat_dal.insert_one_chat({"user": "a"})
    chat_dal.insert_one_chat({"user": "b"})
    all_chats = chat_dal.find_all_chats()
    assert len(all_chats) == 2

def test_chat_update_one(mock_db):
    chat_dal.insert_one_chat({"user": "amy", "mood": "sad"})
    updated = chat_dal.update_one_chat({"user": "amy"}, {"mood": "happy"})
    assert updated is True

def test_chat_delete_one(mock_db):
    chat_dal.insert_one_chat({"id": 1})
    deleted = chat_dal.delete_one_chat({"id": 1})
    assert deleted is True

#message tests
def test_message_insert_one():
    msg_id = messages_dal.insert_one_message({"sender": "user", "content": "hi"})
    assert msg_id != ""

def test_message_find_one(mock_db):
    messages_dal.insert_one_message({"sender": "bot", "content": "welcome"})
    found = messages_dal.find_one_message({"sender": "bot"})
    assert found["sender"] == "bot"

def test_message_find_all(mock_db):
    messages_dal.insert_one_message({"x": 1})
    messages_dal.insert_one_message({"x": 2})
    all_msgs = messages_dal.find_all_messages()
    assert len(all_msgs) == 2

def test_message_update_one(mock_db):
    messages_dal.insert_one_message({"id": 10, "sent": False})
    updated = messages_dal.update_one_message({"id": 10}, {"sent": True})
    assert updated is True

def test_message_delete_one(mock_db):
    messages_dal.insert_one_message({"id": 100})
    deleted = messages_dal.delete_one_message({"id": 100})
    assert deleted is True
