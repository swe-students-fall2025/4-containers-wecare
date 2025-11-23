from flask_cors import CORS
from flask import Flask, render_template, send_from_directory, jsonify, request, Response
import requests
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
    """ home page view """
    return render_template("index.html")

@app.route("/api/messages")
def get_messages():
    """get messages from mongodb"""
    try:
        messages = list(db.messages.find({}, {"_id": 0}))
        return jsonify(messages)
    except Exception as e:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(e)}), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    try:
        # test mongodb connection
        client.admin.command('ping')
        return jsonify({"status": "healthy", "mongodb": "connected"})
    except Exception as e:  # pylint: disable=broad-exception-caught
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/static/<path:path>")
def send_static(path):
    """ static files serve"""
    return send_from_directory("static", path)

# proxy to machine-learning-client no need cors
ML_CLIENT_HOST = os.getenv("ML_CLIENT_HOST", "machine-learning-client")
ML_CLIENT_PORT = os.getenv("ML_CLIENT_PORT", "5050")
ML_BASE_URL = f"http://{ML_CLIENT_HOST}:{ML_CLIENT_PORT}"

def proxy_request(target_url):
    """proxy to backend"""
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Backend service unavailable", "details": str(e)}), 502

@app.route("/chats/api", methods=["GET", "POST"])
@app.route("/chats/api/", methods=["GET", "POST"])
@app.route("/chats/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_chats(path=""):  # pylint: disable=unused-argument
    """ proxy url """
    return proxy_request(f"{ML_BASE_URL}{request.path}")

@app.route("/messages/api", methods=["GET", "POST"])
@app.route("/messages/api/", methods=["GET", "POST"])
@app.route("/messages/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_messages(path=""):  # pylint: disable=unused-argument
    """ proxy messages to backend"""
    return proxy_request(f"{ML_BASE_URL}{request.path}")

@app.route("/speech/api/<path:path>", methods=["POST"])
def proxy_speech(path):  # pylint: disable=unused-argument
    """ proxy audio """
    return proxy_request(f"{ML_BASE_URL}{request.path}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
