from flask import Flask
from flask_cors import CORS
from backend.routers.chat_server import chat_router
from backend.routers.messages_server import messages_router
from backend.routers.speech_server import speech_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# register all blueprints
app.register_blueprint(chat_router)
app.register_blueprint(messages_router)
app.register_blueprint(speech_router)


@app.route("/")
def index():
    """server home page"""
    return {"message": "Machine Learning Client API is running"}


@app.route("/health")
def health_check():
    """check health of the backend"""
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
