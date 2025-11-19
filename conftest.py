import os
import pytest

#` Set environment variables for testing`
os.environ["TESTING"] = "1"
os.environ["MONGO_URI"] = "fake"
os.environ["MONGO_DB"] = "fake"

from tests.fake_backend import FakeDB, fake_ask_model
import backend.DAL as DAL
import backend.fake_DAL as fake_DAL

# Create a single instance of FakeDB to be used in tests
FAKE_DB = FakeDB()


@pytest.fixture(autouse=True)
def mock_backend(monkeypatch, request):

    FAKE_DB.reset()

    monkeypatch.setattr(fake_DAL, "db", FAKE_DB)
    monkeypatch.setattr(DAL, "db", FAKE_DB)

    import backend.routers.chat_server as chat_server
    import backend.routers.messages_server as messages_server
    import backend.routers.model_client as model_client

    monkeypatch.setattr(chat_server, "chat_dal", fake_DAL.chat_dal)
    monkeypatch.setattr(messages_server, "messages_dal", fake_DAL.messages_dal)

    monkeypatch.setattr(chat_server, "ask_model", fake_ask_model)
    monkeypatch.setattr(model_client, "ask_model", fake_ask_model)

    # Seed chat for specific tests
    if request.node.name in {"test_get_chat", "test_update_chat", "test_delete_chat"}:
        FAKE_DB.chats.insert_one({"_id": "123", "text": "hello"})

    # Seed messages for specific tests
    if request.node.name == "test_get_all_chats":
        monkeypatch.setattr(
            fake_DAL.chat_dal,
            "find_all_chats",
            lambda: [{"_id": "dummy", "text": "placeholder"}]
        )

    return FAKE_DB
