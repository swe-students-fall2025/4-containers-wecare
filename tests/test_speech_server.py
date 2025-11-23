"""
Unit tests for the speech server
"""

import io
import os
import sys
import importlib
from unittest.mock import patch, MagicMock
import pytest
from flask import Flask
from backend.routers.speech_server import speech_router


# flask app fixture
@pytest.fixture
def client():
    """
    Create a test client for the speech server Flask app.
    """

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(speech_router)

    with app.test_client() as client:
        yield client


# test cases for speech_server.py
def test_transcribe_fake(client):
    """
    Test fake transcription runs in TESTING mode
    """
    # Fake audio file as bytes
    fake_audio = (io.BytesIO(b"FAKEAUDIO"), "test.wav")

    response = client.post(
        "/speech/api/transcribe",
        content_type="multipart/form-data",
        data={"audio": fake_audio},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["text"] == "FAKE_TRANSCRIPTION"


def test_transcribe_missing_file(client):
    """
    Should return 400 error when no file is sent
    """
    response = client.post("/speech/api/transcribe", data={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_transcribe_production_mode_error():
    """Test transcribe error in production mode"""
    with patch.dict(
        os.environ, {"TESTING": "0", "OPENAI_API_KEY": "SK_fake-key"}
    ), patch(
        "openai.OpenAI"
    ) as MockOpenAI:  # pylint: disable= invalid-name

        mock_client_instance = MagicMock()
        MockOpenAI.return_value = mock_client_instance

        # Mock error
        mock_client_instance.audio.transcriptions.create.side_effect = Exception(
            "API Error"
        )

        if "backend.routers.speech_server" in sys.modules:
            import backend.routers.speech_server

            importlib.reload(backend.routers.speech_server)
        else:
            import backend.routers.speech_server

        from backend.routers.speech_server import speech_router

        app = Flask(__name__)
        app.register_blueprint(speech_router)

        with app.test_client() as client:  # pylint: disable=redefined-outer-name
            fake_audio = (io.BytesIO(b"FAKEAUDIO"), "test.wav")
            response = client.post(
                "/speech/api/transcribe",
                content_type="multipart/form-data",
                data={"audio": fake_audio},
            )

            assert response.status_code == 500
            data = response.get_json()
            assert "failed to transcribe audio" in data["error"]
