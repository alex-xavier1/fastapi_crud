# Test suite for the CRUD operations on the Item module

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
from your_module import get_items, get_item, create_item, update_item, delete_item

def test_get_items(db_session: Session):
    mock_items = [Item(id=1, name="item1"), Item(id=2, name="item2")]
    db_session.query(Item).all.return_value = mock_items
    items = get_items(db_session)
    assert len(items) == 2
    assert items[0].name == "item1"
    assert items[1].name == "item2"

def test_get_item_found(db_session: Session):
    mock_item = Item(id=1, name="item1")
    db_session.query(Item).filter().first.return_value = mock_item
    item = get_item(db_session, 1)
    assert item.id == 1
    assert item.name == "item1"

def test_get_item_not_found(db_session: Session):
    db_session.query(Item).filter().first.return_value = None
    item = get_item(db_session, 1)
    assert item is None

def test_create_item(db_session: Session):
    new_item = ItemCreate(name="new_item")
    db_session.query(Item).filter().first.return_value = None
    created_item = create_item(db_session, new_item)
    assert created_item.name == "new_item"

def test_update_item_found(db_session: Session):
    existing_item = Item(id=1, name="item1")
    db_session.query(Item).filter().first.return_value = existing_item
    updated_item = ItemCreate(name="updated_item")
    result = update_item(db_session, 1, updated_item)
    assert result.name == "updated_item"

def test_update_item_not_found(db_session: Session):
    db_session.query(Item).filter().first.return_value = None
    updated_item = ItemCreate(name="updated_item")
    result = update_item(db_session, 1, updated_item)
    assert result is None

def test_delete_item_found(db_session: Session):
    existing_item = Item(id=1, name="item1")
    db_session.query(Item).filter().first.return_value = existing_item
    result = delete_item(db_session, 1)
    assert result == existing_item

def test_delete_item_not_found(db_session: Session):
    db_session.query(Item).filter().first.return_value = None
    result = delete_item(db_session, 1)
    assert result is None