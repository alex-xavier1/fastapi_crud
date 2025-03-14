# Unit tests for CRUD operations on items

from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
import crud

def test_get_items():
    mock_db = MagicMock(spec=Session)
    mock_items = [Item(id=1, name="item1", description="desc1"), Item(id=2, name="item2", description="desc2")]
    mock_db.query(Item).all.return_value = mock_items
    items = crud.get_items(mock_db)
    assert len(items) == 2
    assert items[0].name == "item1"
    assert items[1].name == "item2"

def test_get_item_found():
    mock_db = MagicMock(spec=Session)
    mock_db.query(Item).filter(Item.id == 1).first.return_value = Item(id=1, name="item1", description="desc1")
    item = crud.get_item(mock_db, 1)
    assert item.name == "item1"

def test_get_item_not_found():
    mock_db = MagicMock(spec=Session)
    mock_db.query(Item).filter(Item.id == 1).first.return_value = None
    item = crud.get_item(mock_db, 1)
    assert item is None

def test_create_item():
    mock_db = MagicMock(spec=Session)
    item_create = ItemCreate(name="new_item", description="new_desc")
    mock_db_item = Item(id=1, name="new_item", description="new_desc")
    mock_db.add(mock_db_item)
    mock_db.commit()
    mock_db.refresh(mock_db_item)
    crud.create_item(mock_db, item_create)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_db_item)

def test_update_item_found():
    mock_db = MagicMock(spec=Session)
    mock_db_item = Item(id=1, name="item1", description="desc1")
    mock_db.query(Item).filter(Item.id == 1).first.return_value = mock_db_item
    item_create = ItemCreate(name="updated_item", description="updated_desc")
    crud.update_item(mock_db, 1, item_create)
    assert mock_db_item.name == "updated_item"
    assert mock_db_item.description == "updated_desc"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_db_item)

def test_update_item_not_found():
    mock_db = MagicMock(spec=Session)
    mock_db.query(Item).filter(Item.id == 1).first.return_value = None
    item_create = ItemCreate(name="updated_item", description="updated_desc")
    updated_item = crud.update_item(mock_db, 1, item_create)
    assert updated_item is None

def test_delete_item_found():
    mock_db = MagicMock(spec=Session)
    mock_db_item = Item(id=1, name="item1", description="desc1")
    mock_db.query(Item).filter(Item.id == 1).first.return_value = mock_db_item
    crud.delete_item(mock_db, 1)
    mock_db.delete.assert_called_once_with(mock_db_item)
    mock_db.commit.assert_called_once()

def test_delete_item_not_found():
    mock_db = MagicMock(spec=Session)
    mock_db.query(Item).filter(Item.id == 1).first.return_value = None
    crud.delete_item(mock_db, 1)
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()