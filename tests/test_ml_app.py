"""
Tests for the main app.py
"""

import pytest
from app import app  # pylint: disable=import-error


@pytest.fixture
def client():
    """Test client fixture"""
    app.config["TESTING"] = True
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        yield client


def test_index(client):  # pylint: disable=redefined-outer-name
    """Test index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Machine Learning Client API is running"}


def test_health(client):  # pylint: disable=redefined-outer-name
    """Test health route"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}
