# Unit tests for FastAPI items module, ensuring proper functionality and error handling

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base, SessionLocal
from crud import create_item as crud_create_item
from schemas import ItemCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

def test_create_item():
    item = ItemCreate(name="Test Item", description="Test Description")
    response = client.post("/items", json=item.dict())
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item():
    item = ItemCreate(name="Test Item", description="Test Description")
    created_item = crud_create_item(db=next(override_get_db()), item=item)
    response = client.get(f"/items/{created_item.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item():
    item = ItemCreate(name="Test Item", description="Test Description")
    created_item = crud_create_item(db=next(override_get_db()), item=item)
    updated_item = ItemCreate(name="Updated Item", description="Updated Description")
    response = client.put(f"/items/{created_item.id}", json=updated_item.dict())
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_update_item_not_found():
    updated_item = ItemCreate(name="Updated Item", description="Updated Description")
    response = client.put("/items/999", json=updated_item.dict())
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item():
    item = ItemCreate(name="Test Item", description="Test Description")
    created_item = crud_create_item(db=next(override_get_db()), item=item)
    response = client.delete(f"/items/{created_item.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted"

def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"