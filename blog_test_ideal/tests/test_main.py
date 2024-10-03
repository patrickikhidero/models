from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

def test_create_post(client):
    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post"
    assert "id" in data

def test_read_posts(client):
    # Create a test post
    client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post"},
    )
    
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Post"

def test_read_post(client):
    # Create a test post
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post"

def test_update_post(client):
    # Create a test post
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    
    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Post", "content": "This is an updated post"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Post"
    assert data["content"] == "This is an updated post"

def test_delete_post(client):
    # Create a test post
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post"},
    )
    post_id = post_response.json()["id"]
    
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 200
    
    # Try to get the deleted post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404