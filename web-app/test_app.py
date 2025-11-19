"""
Unit tests for the web application
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test that the index route returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tech Helper' in response.data


def test_static_files(client):
    """Test that static files are served"""
    response = client.get('/static/css/style.css')
    assert response.status_code == 200


def test_create_chat_endpoint(client, monkeypatch):
    """Test creating a new chat"""
    # Mock the database insert
    def mock_insert(*args, **kwargs):
        return "test_chat_id_123"
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'insert_one_chat', mock_insert)
    
    response = client.post(
        '/chats/api',
        json={'title': 'Test Chat', 'messages': []},
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'inserted_id' in data


def test_get_all_chats(client, monkeypatch):
    """Test getting all chats"""
    # Mock the database query
    def mock_find_all(*args, **kwargs):
        return [
            {'_id': '1', 'title': 'Chat 1', 'messages': []},
            {'_id': '2', 'title': 'Chat 2', 'messages': []}
        ]
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'find_all_chats', mock_find_all)
    
    response = client.get('/chats/api/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_get_single_chat(client, monkeypatch):
    """Test getting a specific chat"""
    # Mock the database query
    def mock_find_one(*args, **kwargs):
        return {
            '_id': 'test_id',
            'title': 'Test Chat',
            'messages': [
                {'role': 'user', 'content': 'Hello'}
            ]
        }
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'find_one_chat', mock_find_one)
    
    response = client.get('/chats/api/test_id')
    assert response.status_code == 200
    data = response.get_json()
    assert data['_id'] == 'test_id'
    assert len(data['messages']) == 1


def test_chat_not_found(client, monkeypatch):
    """Test getting a non-existent chat"""
    # Mock the database query to return None
    def mock_find_one(*args, **kwargs):
        return None
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'find_one_chat', mock_find_one)
    
    response = client.get('/chats/api/nonexistent_id')
    assert response.status_code == 404


def test_update_chat(client, monkeypatch):
    """Test updating a chat"""
    # Mock the database update
    def mock_update(*args, **kwargs):
        return True
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'update_one_chat', mock_update)
    
    response = client.put(
        '/chats/api/test_id',
        json={'title': 'Updated Title'},
        content_type='application/json'
    )
    assert response.status_code == 200


def test_delete_chat(client, monkeypatch):
    """Test deleting a chat"""
    # Mock the database delete
    def mock_delete(*args, **kwargs):
        return True
    
    from backend import DAL
    monkeypatch.setattr(DAL.chat_dal, 'delete_one_chat', mock_delete)
    
    response = client.delete('/chats/api/test_id')
    assert response.status_code == 200


def test_create_message(client, monkeypatch):
    """Test creating a message"""
    # Mock the database insert
    def mock_insert(*args, **kwargs):
        return "test_message_id_456"
    
    from backend import DAL
    monkeypatch.setattr(DAL.messages_dal, 'insert_one_message', mock_insert)
    
    response = client.post(
        '/messages/api',
        json={
            'chat_id': 'test_chat',
            'role': 'user',
            'content': 'Test message'
        },
        content_type='application/json'
    )
    assert response.status_code == 201


def test_invalid_json(client):
    """Test sending invalid JSON"""
    response = client.post(
        '/chats/api',
        data='invalid json',
        content_type='application/json'
    )
    # Should return 400 or 500 depending on error handling
    assert response.status_code in [400, 500]