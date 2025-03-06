# ```python

# Testing Item and Task models in FastAPI

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.models import Item, Task
from app.main import app, get_db

# Mocking database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependencies for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Mock Item and Task for testing
@pytest.fixture
def test_item():
    return Item(id=1, name="Test Item", description="This is a test item", price=10, quantity=5)

@pytest.fixture
def test_task():
    return Task(id=1, name="Test Task")

# Test Item model
def test_create_item(test_item):
    response = client.post("/items/", json=test_item.dict())
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "description": "This is a test item", "price": 10, "quantity": 5}

# Test Task model
def test_create_task(test_task):
    response = client.post("/tasks/", json=test_task.dict())
    assert response.status_code == 200
    assert response.json() == {"name": "Test Task"}

# Test edge cases
def test_create_item_no_name(test_item):
    test_item.name = None
    response = client.post("/items/", json=test_item.dict())
    assert response.status_code == 422

def test_create_task_no_name(test_task):
    test_task.name = None
    response = client.post("/tasks/", json=test_task.dict())
    assert response.status_code == 422
```