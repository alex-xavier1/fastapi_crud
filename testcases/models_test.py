# ```python

# Unit tests for Item and Task models in FastAPI
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock

from model import Item, Task, Base

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_item_model():
    with patch('model.Item') as mock:
        item = Item(id=1, name='item1', description='desc1', price=10, quantity=5)
        mock.return_value = item
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "item1", "description": "desc1", "price": 10, "quantity": 5}

def test_task_model():
    with patch('model.Task') as mock:
        task = Task(id=1, name='task1')
        mock.return_value = task
        response = client.get("/tasks/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "task1"}

def test_item_not_found():
    with patch('model.Item') as mock:
        mock.return_value = None
        response = client.get("/items/999")
        assert response.status_code == 404

def test_task_not_found():
    with patch('model.Task') as mock:
        mock.return_value = None
        response = client.get("/tasks/999")
        assert response.status_code == 404
```