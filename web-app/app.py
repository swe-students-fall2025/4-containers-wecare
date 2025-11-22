"""
Main application file for the web app.
"""

from flask_cors import CORS
from flask import Flask, render_template, send_from_directory, jsonify
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)
CORS(app)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://root:example@mongodb:27017/")
client = MongoClient(mongo_uri)
db = client["chat_app"]

@app.route("/")
def index():
    """
    Render the main index page.
    """
    return render_template("index.html")

@app.route("/api/messages")
def get_messages():
    """get messages from mongodb"""
    try:
        messages = list(db.messages.find({}, {"_id": 0}))
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({"status": "healthy", "mongodb": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/static/<path:path>")
def send_static(path):
    """
    Serve static files.
    """
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
