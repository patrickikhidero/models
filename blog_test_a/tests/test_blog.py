import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import models
from app.database import Base, get_db

# Mocking SQLAlchemy session
@pytest.fixture
def mock_db_session(mocker):
    return mocker.Mock(spec=Session)

client = TestClient(app)

# Mocking database operations
@pytest.fixture
def mock_crud(mocker):
    mocker.patch('app.crud.get_post', return_value=models.Post(id=1, title="Test", content="Test content"))
    mocker.patch('app.crud.create_post', return_value=models.Post(id=1, title="New Test", content="New content"))

def test_create_post(mock_db_session, mock_crud):
    response = client.post("/posts/", json={"title": "New Test", "content": "New content"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Test"

def test_read_post(mock_db_session, mock_crud):
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Similar tests for update and delete can be added here
