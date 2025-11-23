"""
Tests for model_client.py
"""

# pylint: disable=duplicate-code


import os
import sys
from unittest.mock import patch, MagicMock
import importlib


def test_ask_model_testing_mode():
    """Test ask_model in testing mode"""
    # make sure testong is set to 1
    with patch.dict(os.environ, {"TESTING": "1"}):
        # reload to pick up the env var
        if "backend.routers.model_client" in sys.modules:
            module = importlib.reload(sys.modules["backend.routers.model_client"])
        else:
            module = importlib.import_module("backend.routers.model_client")

        ask_model = module.ask_model

        response = ask_model([])
        assert response == "FAKE_MODEL_RESPONSE"


def test_ask_model_production_mode_error():
    """Test ask_model error handling in production mode"""
    with patch.dict(
        os.environ, {"TESTING": "0", "OPENAI_API_KEY": "SK_fake-key"}
    ), patch(
        "openai.OpenAI"
    ) as MockOpenAI:  # pylint: disable=invalid-name

        mock_client_instance = MagicMock()
        MockOpenAI.return_value = mock_client_instance

        # make method raise exception
        mock_client_instance.chat.completions.create.side_effect = Exception(
            "API Error"
        )

        if "backend.routers.model_client" in sys.modules:
            module = importlib.reload(sys.modules["backend.routers.model_client"])
        else:
            module = importlib.import_module("backend.routers.model_client")

        ask_model = module.ask_model

        response = ask_model([{"role": "user", "content": "hello"}])
        assert "Sorry, ai is not working right now" in response
