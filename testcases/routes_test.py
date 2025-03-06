# ```python

from unittest.mock import patch, MagicMock
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_db
from database import SessionLocal
import crud, schemas


client = TestClient(app)


@patch("main.crud")
@patch("main.get_db")
def test_read_items(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.get_items.return_value = []

    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


@patch("main.crud")
@patch("main.get_db")
def test_read_item_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.get_item.return_value = schemas.ItemResponse(id=1, name="test", price=10.0)

    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "test", "price": 10.0}


@patch("main.crud")
@patch("main.get_db")
def test_read_item_not_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.get_item.return_value = None

    response = client.get("/items/1")

    assert response.status_code == 404


@patch("main.crud")
@patch("main.get_db")
def test_create_item(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.create_item.return_value = schemas.ItemResponse(id=1, name="test", price=10.0)

    response = client.post("/items", json={"name": "test", "price": 10.0})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "test", "price": 10.0}


@patch("main.crud")
@patch("main.get_db")
def test_update_item_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.update_item.return_value = schemas.ItemResponse(id=1, name="updated", price=15.0)

    response = client.put("/items/1", json={"name": "updated", "price": 15.0})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "updated", "price": 15.0}


@patch("main.crud")
@patch("main.get_db")
def test_update_item_not_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.update_item.return_value = None

    response = client.put("/items/1", json={"name": "updated", "price": 15.0})

    assert response.status_code == 404


@patch("main.crud")
@patch("main.get_db")
def test_delete_item_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.delete_item.return_value = {"detail": "Item deleted"}

    response = client.delete("/items/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Item deleted"}


@patch("main.crud")
@patch("main.get_db")
def test_delete_item_not_found(mock_get_db, mock_crud):
    mock_get_db.return_value = MagicMock(spec=Session)
    mock_crud.delete_item.return_value = None

    response = client.delete("/items/1")

    assert response.status_code == 404
```