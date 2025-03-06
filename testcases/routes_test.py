# ```python

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from main import app, get_db
from crud import get_item, get_items, create_item, update_item, delete_item
import schemas

client = TestClient(app)

# Mock the get_db dependency
app.dependency_overrides[get_db] = MagicMock()

def test_read_items():
    with patch.object(get_items, "return_value", [{"name": "item1", "description": "description1"}]):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == [{"name": "item1", "description": "description1"}]

def test_read_item():
    with patch.object(get_item, "return_value", {"name": "item1", "description": "description1"}):
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {"name": "item1", "description": "description1"}

    with patch.object(get_item, "return_value", None):
        response = client.get("/items/99")
        assert response.status_code == 404

def test_create_item():
    test_item = schemas.ItemCreate(name="item1", description="description1")
    with patch.object(create_item, "return_value", test_item):
        response = client.post("/items", json={"name": "item1", "description": "description1"})
        assert response.status_code == 200
        assert response.json() == {"name": "item1", "description": "description1"}

def test_update_item():
    test_item = schemas.ItemCreate(name="item1", description="description1")
    with patch.object(update_item, "return_value", test_item):
        response = client.put("/items/1", json={"name": "item1", "description": "description1"})
        assert response.status_code == 200
        assert response.json() == {"name": "item1", "description": "description1"}

    with patch.object(update_item, "return_value", None):
        response = client.put("/items/99", json={"name": "item1", "description": "description1"})
        assert response.status_code == 404

def test_delete_item():
    with patch.object(delete_item, "return_value", {"detail": "Item deleted"}):
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {"detail": "Item deleted"}

    with patch.object(delete_item, "return_value", None):
        response = client.delete("/items/99")
        assert response.status_code == 404
```