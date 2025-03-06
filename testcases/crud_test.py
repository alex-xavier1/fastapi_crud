# ```python

# This file contains unit tests for the item management module using FastAPI and SQLAlchemy

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import patch, MagicMock
from models import Item
from schemas import ItemCreate
import item_management

# Mocking the SQLAlchemy Session
SessionLocalMock = MagicMock(spec=Session)

@pytest.fixture
def db():
    return SessionLocalMock()

# Mocking a sample item
@pytest.fixture
def item():
    return ItemCreate(name="Test", description="Test item", price=10.0)

# Mocking the SQLAlchemy Item model
@pytest.fixture
def db_item():
    return Item(id=1, name="Test", description="Test item", price=10.0)

def test_get_items(db):
    with patch.object(db, 'query', return_value=[db_item]) as mock_query:
        result = item_management.get_items(db)
    mock_query.assert_called_once_with(Item)
    assert result == [db_item]

def test_get_item(db, db_item):
    with patch.object(db, 'query', return_value=db_item) as mock_query:
        result = item_management.get_item(db, db_item.id)
    mock_query.assert_called_once_with(Item)
    assert result == db_item

def test_create_item(db, item, db_item):
    with patch.object(db, 'add'), patch.object(db, 'commit'), patch.object(db, 'refresh'):
        result = item_management.create_item(db, item)
        db.add.assert_called_once_with(db_item)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(db_item)
        assert result == db_item

def test_update_item(db, item, db_item):
    with patch.object(db, 'query', return_value=db_item), patch.object(db, 'commit'), patch.object(db, 'refresh'):
        result = item_management.update_item(db, db_item.id, item)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(db_item)
        assert result == db_item

def test_delete_item(db, db_item):
    with patch.object(db, 'delete'), patch.object(db, 'commit'):
        result = item_management.delete_item(db, db_item.id)
        db.delete.assert_called_once_with(db_item)
        db.commit.assert_called_once()
        assert result == db_item
```