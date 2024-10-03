import pytest
from app import crud

def test_create_post(client):
    response = client.post("/posts/", json={"title": "test", "content": "test content", "author": "test author"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "test"
    assert "id" in data

def test_read_post(client, db):
    new_post = crud.create_post(db, schemas.PostCreate(title="Read Test", content="Content", author="Author"))
    response = client.get(f"/posts/{new_post.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read Test"

def test_update_post(client, db):
    new_post = crud.create_post(db, schemas.PostCreate(title="Update Test", content="Content", author="Author"))
    response = client.put(f"/posts/{new_post.id}", json={"title": "Updated", "content": "Updated Content", "author": "New Author"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_delete_post(client, db):
    new_post = crud.create_post(db, schemas.PostCreate(title="Delete Test", content="Content", author="Author"))
    response = client.delete(f"/posts/{new_post.id}")
    assert response.status_code == 204
    response = client.get(f"/posts/{new_post.id}")
    assert response.status_code == 404

def test_read_nonexistent_post(client):
    response = client.get("/posts/999")
    assert response.status_code == 404