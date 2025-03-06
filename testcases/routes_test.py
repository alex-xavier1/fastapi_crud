# ```python

# Unit tests for FastAPI routing module

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from database import SessionLocal
from unittest.mock import patch, MagicMock
import pytest
import main

client = TestClient(main.app)

def override_get_db():
    return SessionLocal()

main.app.dependency_overrides[main.get_db] = override_get_db


def test_read_items():
    with patch('main.crud.get_items', return_value=[{'id': 1, 'name': 'test item', 'description': 'test'}]) as mock:
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == [{'id': 1, 'name': 'test item', 'description': 'test'}]
        mock.assert_called_once()


def test_read_item():
    with patch('main.crud.get_item', return_value={'id': 1, 'name': 'test item', 'description': 'test'}) as mock:
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'test item', 'description': 'test'}
        mock.assert_called_once_with(1)

    with patch('main.crud.get_item', return_value=None) as mock:
        response = client.get("/items/999")
        assert response.status_code == 404
        assert response.json() == {'detail': 'Item not found'}
        mock.assert_called_once_with(999)


def test_create_item():
    with patch('main.crud.create_item', return_value={'id': 1, 'name': 'test item', 'description': 'test'}) as mock:
        response = client.post("/items", json={'name': 'test item', 'description': 'test'})
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'test item', 'description': 'test'}
        mock.assert_called_once()


def test_update_item():
    with patch('main.crud.update_item', return_value={'id': 1, 'name': 'updated item', 'description': 'updated'}) as mock:
        response = client.put("/items/1", json={'name': 'updated item', 'description': 'updated'})
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'name': 'updated item', 'description': 'updated'}
        mock.assert_called_once()

    with patch('main.crud.update_item', return_value=None) as mock:
        response = client.put("/items/999", json={'name': 'updated item', 'description': 'updated'})
        assert response.status_code == 404
        assert response.json() == {'detail': 'Item not found'}
        mock.assert_called_once()


def test_delete_item():
    with patch('main.crud.delete_item', return_value=1) as mock:
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {'detail': 'Item deleted'}
        mock.assert_called_once()

    with patch('main.crud.delete_item', return_value=None) as mock:
        response = client.delete("/items/999")
        assert response.status_code == 404
        assert response.json() == {'detail': 'Item not found'}
        mock.assert_called_once()
```