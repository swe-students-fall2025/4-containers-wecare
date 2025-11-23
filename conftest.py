"""
Conftest module to set up test environment and mock backend components.
"""

import os
import sys
import pytest

# set environment variables for testing
os.environ["TESTING"] = "1"
os.environ["MONGO_URI"] = "fake"
os.environ["MONGO_DB"] = "fake"

# make sure we can import the backend modules
ROOT = os.path.abspath(os.path.dirname(__file__))
ML_CLIENT = os.path.join(ROOT, "machine-learning-client")

sys.path.insert(0, ML_CLIENT)
sys.path.insert(0, ROOT)


# import fake backend components
from tests.fake_backend import FakeDB, fake_ask_model
import backend.fake_DAL as fake_DAL
import backend.DAL as DAL


# Shared fake DB instance
FAKE_DB = FakeDB()


@pytest.fixture(autouse=True)
def mock_backend(monkeypatch, request):
    """
    Fixture to mock backend components for testing.
    """
    FAKE_DB.reset()

    # Patch DB instances
    monkeypatch.setattr(fake_DAL, "db", FAKE_DB)
    monkeypatch.setattr(DAL, "db", FAKE_DB)

    # Routers
    import backend.routers.chat_server as chat_server
    import backend.routers.messages_server as messages_server
    import backend.routers.model_client as model_client

    # Patch DALs
    monkeypatch.setattr(chat_server, "chat_dal", fake_DAL.chat_dal)
    monkeypatch.setattr(messages_server, "messages_dal", fake_DAL.messages_dal)

    # Patch model client
    monkeypatch.setattr(chat_server, "ask_model", fake_ask_model)
    monkeypatch.setattr(model_client, "ask_model", fake_ask_model)

    # Seed chat for specific tests
    if request.node.name in {
        "test_get_chat",
        "test_update_chat",
        "test_delete_chat",
        "test_send_message",
    }:
        FAKE_DB.chats.insert_one({"_id": "123", "text": "hello"})

    # Seed chats for list test
    if request.node.name == "test_get_all_chats":
        monkeypatch.setattr(
            fake_DAL.chat_dal,
            "find_all_chats",
            lambda: [{"_id": "dummy", "text": "placeholder"}],
        )

    return FAKE_DB
