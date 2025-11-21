import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from backend.routers.chat_server import chat_router
from backend.routers.messages_server import messages_router

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(chat_router)
app.register_blueprint(messages_router)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
