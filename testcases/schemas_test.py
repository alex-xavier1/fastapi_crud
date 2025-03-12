# Unit tests for Item models ensuring correct validation and behavior

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, create_item, get_db
from models import ItemBase, ItemCreate, ItemResponse

client = TestClient(app)

def test_item_create_model():
    item = ItemCreate(name="Test Item", description="A test item", price=100, quantity=50)
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 100
    assert item.quantity == 50

def test_item_response_model():
    item = ItemResponse(id=1, name="Test Item", description="A test item", price=100, quantity=50)
    assert item.id == 1
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 100
    assert item.quantity == 50

@patch('main.get_db')
def test_create_item_endpoint(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_db.query().filter().first.return_value = None
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    response = client.post("/items/", json={"name": "Test Item", "description": "A test item", "price": 100, "quantity": 50})
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert data["price"] == 100
    assert data["quantity"] == 50
    assert "id" in data

def test_create_item_endpoint_invalid_data():
    response = client.post("/items/", json={"name": "", "description": "A test item", "price": 100, "quantity": 50})
    assert response.status_code == 422