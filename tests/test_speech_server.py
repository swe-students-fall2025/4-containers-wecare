"""
Unit tests for the speech server
"""

import io
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

#test cases for speech_server.py
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
