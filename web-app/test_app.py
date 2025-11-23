"""
Unit tests for the web application
"""

import sys  # pylint: disable=unused-import
from unittest.mock import MagicMock, Mock, patch  # pylint: disable=unused-import
import requests
import pytest
from app import app as flask_app
from app import db  # pylint: disable=unused-import


@pytest.fixture
def app():
    """create application for the tests."""

    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield flask_app


def test_index_route(client):
    """test that the index route returns 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Tech Helper" in response.data


def test_static_files(client):
    """Test that static files are served"""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200


def test_create_chat_endpoint(client, monkeypatch):
    """Test creating a new chat"""

    # mock requests.request
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.content = b'{"inserted_id": "test_chat_id_123"}'
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.post(
        "/chats/api",
        json={"title": "Test Chat", "messages": []},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "inserted_id" in data


def test_get_all_chats(client, monkeypatch):
    """Test getting all chats"""

    # mock requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'[{"_id": "1", "title": "Chat 1", "messages": []}, {"_id": "2", "title": "Chat 2", "messages": []}]'  # pylint: disable=line-too-long
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.get("/chats/api/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_get_single_chat(client, monkeypatch):
    """Test getting a specific chat"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'{"_id": "test_id", "title": "Test Chat", "messages": [{"role": "user", "content": "Hello"}]}'  # pylint: disable=line-too-long
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.get("/chats/api/test_id")
    assert response.status_code == 200
    data = response.get_json()
    assert data["_id"] == "test_id"
    assert len(data["messages"]) == 1


def test_chat_not_found(client, monkeypatch):
    """Test getting a non-existent chat"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.content = b'{"error": "Chat not found"}'
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.get("/chats/api/nonexistent_id")
    assert response.status_code == 404


def test_update_chat(client, monkeypatch):
    """Test updating a chat"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'{"status": "success"}'
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.put(
        "/chats/api/test_id",
        json={"title": "Updated Title"},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_chat(client, monkeypatch):
    """Test deleting a chat"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'{"status": "success"}'
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.delete("/chats/api/test_id")
    assert response.status_code == 200


def test_create_message(client, monkeypatch):
    """Test creating a message"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.content = b'{"inserted_id": "test_message_id_456"}'
    mock_response.raw.headers = {"Content-Type": "application/json"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.post(
        "/messages/api",
        json={"chat_id": "test_chat", "role": "user", "content": "Test message"},
        content_type="application/json",
    )
    assert response.status_code == 201


def test_get_messages(client, monkeypatch):  # pylint: disable=unused-argument
    """Test getting messages from mongodb"""

    # Mock pymongo
    mock_db = Mock()
    mock_db.messages.find.return_value = [{"content": "msg1"}, {"content": "msg2"}]

    with patch("app.db", mock_db):
        response = client.get("/api/messages")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2


def test_proxy_speech(client, monkeypatch):
    """Test proxy speech endpoint"""

    # Mock requests.request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"audio_data"
    mock_response.raw.headers = {"Content-Type": "audio/mpeg"}

    mock_request = Mock(return_value=mock_response)

    monkeypatch.setattr(requests, "request", mock_request)

    response = client.post("/speech/api/generate")
    assert response.status_code == 200
    assert response.data == b"audio_data"
