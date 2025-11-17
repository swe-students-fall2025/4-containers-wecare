# backend/model_client.py
import requests
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


MODEL_URL = os.getenv("MODEL_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def ask_model(messages):

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
    }

    resp = requests.post(MODEL_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"]
