"""
Speech server router for handling audio transcription requests.
"""

import os
import tempfile

from flask import Blueprint, jsonify, request
from flask import Blueprint, jsonify, request
from openai import OpenAI
from werkzeug.utils import secure_filename

TESTING = os.environ.get("TESTING") == "1"

speech_router = Blueprint("speech", __name__, url_prefix="/speech/api")

if TESTING:
    # Fake speech transcription during tests
    @speech_router.post("/transcribe")
    def fake_transcribe():
        """
        Fake transcription endpoint for testing
        """
        # If no file sent → 400
        if "audio" not in request.files:
            return jsonify({"error": "no audio file given"}), 400

        return jsonify({"text": "FAKE_TRANSCRIPTION"}), 200

else:
    # open ai setup
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("PLEASE SETUP OPEN AI KEY IN THE .env")

    client = OpenAI(api_key=api_key)

    speech_router = Blueprint("speech", __name__, url_prefix="/speech/api")

    @speech_router.post("/transcribe")
    def transcribe_audio():
        """
        gets audio and return it as text
        """
        if "audio" not in request.files:
            return jsonify({"error": "no audio file given"}), 400
        audio_file = request.files["audio"]
        if audio_file.filename == "":
            return jsonify({"error": "no audio file"}), 400

        temp_path = None

        try:
            # temp files to send to oai
            temp_dir = tempfile.gettempdir()
            filename = secure_filename(audio_file.filename)
            temp_path = os.path.join(temp_dir, filename)
            audio_file.save(temp_path)
            # check if saved temp audio file
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                return (
                    jsonify({"error": "Audio file is empty or could not be saved"}),
                    400,
                )

            # transcribe audio using openai
            with open(temp_path, "rb") as f:
                transcript_text = client.audio.transcriptions.create(
                    model="whisper-1", file=f, response_format="text"
                )

            return jsonify({"transcript": transcript_text})
        except Exception as e: # pylint: disable=broad-exception-caught
            return jsonify({"error": f"failed to transcribe audio: {str(e)}"}), 500
        finally:
            # clean up temp file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e: # pylint: disable=broad-exception-caught
                    print(f"could not remove temp file {temp_path}: {e}")
