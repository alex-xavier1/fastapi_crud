# ```python

# Unit tests for item CRUD operations

from unittest import mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_items, get_item, create_item, update_item, delete_item
from models import Item
from schemas import ItemCreate

client = TestClient(app)

def test_get_items():
    with mock.patch.object(Session, 'query') as mock_query:
        mock_query.return_value.all.return_value = [Item(id=1, name='test', description='test', price=10)]
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == [{'id': 1, 'name': 'test', 'description': 'test', 'price': 10}]

def test_get_item():
    with mock.patch.object(Session, 'query') as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = Item(id=1, name='test', description='test', price=10)
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'test', 'description': 'test', 'price': 10}

def test_create_item():
    with mock.patch.object(Session, 'add') as mock_add, mock.patch.object(Session, 'commit') as mock_commit, mock.patch.object(Session, 'refresh') as mock_refresh:
        mock_item = ItemCreate(name='test', description='test', price=10)
        response = client.post("/items/", json=mock_item.dict())
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'test', 'description': 'test', 'price': 10}

def test_update_item():
    with mock.patch.object(Session, 'query') as mock_query, mock.patch.object(Session, 'commit') as mock_commit, mock.patch.object(Session, 'refresh') as mock_refresh:
        mock_item = ItemCreate(name='updated_test', description='updated_test', price=20)
        response = client.put("/items/1", json=mock_item.dict())
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'updated_test', 'description': 'updated_test', 'price': 20}

def test_delete_item():
    with mock.patch.object(Session, 'query') as mock_query, mock.patch.object(Session, 'delete') as mock_delete, mock.patch.object(Session, 'commit') as mock_commit:
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'test', 'description': 'test', 'price': 10}
```
Note: These unit tests make use of the mock library to replace the ORM Session object methods with mock objects. Each mock object is set to return a specific value when called, which allows the tests to focus on the functionality of the route handlers without relying on an actual database. This approach can be extended to handle more complex scenarios, such as testing error handling code by having the mock objects raise exceptions.