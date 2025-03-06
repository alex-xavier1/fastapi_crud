# ```python

from unittest.mock import patch
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app, get_items, get_item, create_item, update_item, delete_item
from models import Item
from schemas import ItemCreate

client = TestClient(app)

def test_get_items():
    with patch.object(Session, 'query') as mock_query:
        mock_query.return_value.all.return_value = [Item(id=1, name='Test', description='Test item', price=10.0)]
        response = get_items(Session())
        assert response == [{'id': 1, 'name': 'Test', 'description': 'Test item', 'price': 10.0}]

def test_get_item():
    with patch.object(Session, 'query') as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = Item(id=1, name='Test', description='Test item', price=10.0)
        response = get_item(Session(), 1)
        assert response == {'id': 1, 'name': 'Test', 'description': 'Test item', 'price': 10.0}

def test_get_item_not_found():
    with patch.object(Session, 'query') as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException):
            get_item(Session(), 99)

def test_create_item():
    with patch.object(Session, 'add') as mock_add, \
         patch.object(Session, 'commit') as mock_commit, \
         patch.object(Session, 'refresh') as mock_refresh:
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None
        response = create_item(Session(), ItemCreate(name='Test', description='Test item', price=10.0))
        assert response == {'name': 'Test', 'description': 'Test item', 'price': 10.0}

def test_update_item():
    with patch.object(Session, 'query') as mock_query, \
         patch.object(Session, 'commit') as mock_commit, \
         patch.object(Session, 'refresh') as mock_refresh:
        mock_query.return_value.filter.return_value.first.return_value = Item(id=1, name='Old', description='Old item', price=10.0)
        mock_commit.return_value = None
        mock_refresh.return