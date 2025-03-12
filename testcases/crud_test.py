# Test module for CRUD operations on items in FastAPI application

from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
import crud

def test_get_items():
    db_mock = MagicMock(spec=Session)
    items = [Item(id=1, name="item1", description="desc1"), Item(id=2, name="item2", description="desc2")]
    db_mock.query(Item).all.return_value = items
    result = crud.get_items(db_mock)
    assert len(result) == 2
    assert result[0].name == "item1"
    assert result[1].name == "item2"

def test_get_item_found():
    db_mock = MagicMock(spec=Session)
    item = Item(id=1, name="item1", description="desc1")
    db_mock.query(Item).filter(Item.id == 1).first.return_value = item
    result = crud.get_item(db_mock, 1)
    assert result.name == "item1"

def test_get_item_not_found():
    db_mock = MagicMock(spec=Session)
    db_mock.query(Item).filter(Item.id == 1).first.return_value = None
    result = crud.get_item(db_mock, 1)
    assert result is None

def test_create_item():
    db_mock = MagicMock(spec=Session)
    item_create = ItemCreate(name="new_item", description="new_desc")
    db_item = Item(id=3, name="new_item", description="new_desc")
    db_mock.add(db_item)
    db_mock.commit()
    db_mock.refresh(db_item)
    result = crud.create_item(db_mock, item_create)
    assert result.name == "new_item"

def test_update_item_found():
    db_mock = MagicMock(spec=Session)
    item_create = ItemCreate(name="updated_item", description="updated_desc")
    db_item = Item(id=1, name="item1", description="desc1")
    db_mock.query(Item).filter(Item.id == 1).first.return_value = db_item
    crud.update_item(db_mock, 1, item_create)
    assert db_item.name == "updated_item"

def test_update_item_not_found():
    db_mock = MagicMock(spec=Session)
    item_create = ItemCreate(name="updated_item", description="updated_desc")
    db_mock.query(Item).filter(Item.id == 1).first.return_value = None
    result = crud.update_item(db_mock, 1, item_create)
    assert result is None

def test_delete_item_found():
    db_mock = MagicMock(spec=Session)
    db_item = Item(id=1, name="item1", description="desc1")
    db_mock.query(Item).filter(Item.id == 1).first.return_value = db_item
    result = crud.delete_item(db_mock, 1)
    assert result.name == "item1"

def test_delete_item_not_found():
    db_mock = MagicMock(spec=Session)
    db_mock.query(Item).filter(Item.id == 1).first.return_value = None
    result = crud.delete_item(db_mock, 1)
    assert result is None