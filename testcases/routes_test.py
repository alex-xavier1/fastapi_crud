# Unit tests for the items module, covering CRUD operations and error handling

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import crud, schemas
from main import app  # Assuming the FastAPI app is in a file named main.py

client = TestClient(app)

def test_read_items():
    with patch("crud.get_items") as mock_get_items:
        mock_get_items.return_value = [schemas.ItemResponse(id=1, name="Item1", description="Desc1")]
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == [{"id": 1, "name": "Item1", "description": "Desc1"}]

def test_read_item_found():
    with patch("crud.get_item") as mock_get_item:
        mock_get_item.return_value = schemas.ItemResponse(id=1, name="Item1", description="Desc1")
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Item1", "description": "Desc1"}

def test_read_item_not_found():
    with patch("crud.get_item") as mock_get_item:
        mock_get_item.return_value = None
        response = client.get("/items/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

def test_create_item():
    with patch("crud.create_item") as mock_create_item:
        mock_create_item.return_value = schemas.ItemResponse(id=1, name="Item1", description="Desc1")
        response = client.post("/items", json={"name": "Item1", "description": "Desc1"})
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Item1", "description": "Desc1"}

def test_update_item_found():
    with patch("crud.update_item") as mock_update_item:
        mock_update_item.return_value = schemas.ItemResponse(id=1, name="UpdatedItem", description="UpdatedDesc")
        response = client.put("/items/1", json={"name": "UpdatedItem", "description": "UpdatedDesc"})
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "UpdatedItem", "description": "UpdatedDesc"}

def test_update_item_not_found():
    with patch("crud.update_item") as mock_update_item:
        mock_update_item.return_value = None
        response = client.put("/items/1", json={"name": "UpdatedItem", "description": "UpdatedDesc"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}

def test_delete_item_found():
    with patch("crud.delete_item") as mock_delete_item:
        mock_delete_item.return_value = schemas.ItemResponse(id=1, name="Item1", description="Desc1")
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {"detail": "Item deleted"}

def test_delete_item_not_found():
    with patch("crud.delete_item") as mock_delete_item:
        mock_delete_item.return_value = None
        response = client.delete("/items/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}