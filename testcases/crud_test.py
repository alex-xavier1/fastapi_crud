# ```python

import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from models import Item
from schemas import ItemCreate
import crud

# Test file for CRUD operations on Item model

@pytest.fixture
def fake_db():
    return MagicMock(spec=Session)

@pytest.fixture
def fake_item():
    return Item(id=1, name='test_item', price=100)

@pytest.fixture
def fake_item_create():
    return ItemCreate(name='test_item', price=100)

def test_get_items(fake_db):
    crud.get_items(fake_db)
    fake_db.query.assert_called_with(Item)
    fake_db.query().all.assert_called_once()

def test_get_item(fake_db, fake_item):
    fake_db.query().filter().first.return_value = fake_item
    result = crud.get_item(fake_db, 1)
    fake_db.query.assert_called_with(Item)
    fake_db.query().filter.assert_called_once()
    assert result == fake_item

def test_get_item_not_found(fake_db):
    fake_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        crud.get_item(fake_db, 99)

def test_create_item(fake_db, fake_item, fake_item_create):
    fake_db.query().filter().first.return_value = fake_item
    result = crud.create_item(fake_db, fake_item_create)
    fake_db.add.assert_called_once_with(fake_item)
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once_with(fake_item)
    assert result == fake_item

def test_update_item(fake_db, fake_item, fake_item_create):
    fake_db.query().filter().first.return_value = fake_item
    result = crud.update_item(fake_db, 1, fake_item_create)
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once_with(fake_item)
    assert result == fake_item

def test_update_item_not_found(fake_db, fake_item_create):
    fake_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        crud.update_item(fake_db, 99, fake_item_create)

def test_delete_item(fake_db, fake_item):
    fake_db.query().filter().first.return_value = fake_item
    result = crud.delete_item(fake_db, 1)
    fake_db.delete.assert_called_once_with(fake_item)
    fake_db.commit.assert_called_once()
    assert result == fake_item

def test_delete_item_not_found(fake_db):
    fake_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        crud.delete_item(fake_db, 99)
```