"""
Router for model client interactions.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

TESTING = os.environ.get("TESTING") == "1"

if TESTING:
    # Fake model for ALL tests
    def ask_model(messages):  # pylint: disable=unused-argument
        """fak model response"""
        return "FAKE_MODEL_RESPONSE"

else:

    # load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL_NAME = os.getenv("MODEL_NAME")
    MODEL_MAX_NEW_TOKENS = int(os.getenv("MODEL_MAX_NEW_TOKENS", "256"))
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.4"))

    if not client.api_key:
        print("OPENAI_API_KEY is missing or empty please add it to the .env")

    def ask_model(messages):
        """
        send message to open ai and return models resposne
        """
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=MODEL_MAX_NEW_TOKENS,
                temperature=MODEL_TEMPERATURE,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"There was an error getting ai response: {e}")
            return "Sorry, ai is not working right now. Try later!"
