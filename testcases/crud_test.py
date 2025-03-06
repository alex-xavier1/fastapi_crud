# ```python

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
from main import get_items, get_item, create_item, update_item, delete_item

def test_get_items():
    db = Mock(spec=Session)
    db.query.return_value.all.return_value = [Item(id=1, name="Item 1")]

    result = get_items(db)

    db.query.assert_called_once_with(Item)
    db.query.return_value.all.assert_called_once()
    assert result == [Item(id=1, name="Item 1")]


def test_get_item():
    db = Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="Item 1")

    result = get_item(db, 1)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    assert result == Item(id=1, name="Item 1")


def test_get_item_not_found():
    db = Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    result = get_item(db, 1)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    assert result is None


def test_create_item():
    db = Mock(spec=Session)
    item = ItemCreate(name="New item")

    with patch('models.Item', return_value=Item(id=1, name="New item")) as mock_item:
        result = create_item(db, item)

    db.add.assert_called_once_with(mock_item.return_value)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(mock_item.return_value)
    assert result == mock_item.return_value


def test_update_item():
    db = Mock(spec=Session)
    item = ItemCreate(name="Updated item")
    db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="Item 1")

    result = update_item(db, 1, item)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(db.query.return_value.filter.return_value.first.return_value)
    assert result == db.query.return_value.filter.return_value.first.return_value


def test_update_item_not_found():
    db = Mock(spec=Session)
    item = ItemCreate(name="Updated item")
    db.query.return_value.filter.return_value.first.return_value = None

    result = update_item(db, 1, item)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    assert result is None


def test_delete_item():
    db = Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="Item 1")

    result = delete_item(db, 1)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    db.delete.assert_called_once_with(db.query.return_value.filter.return_value.first.return_value)
    db.commit.assert_called_once()
    assert result == db.query.return_value.filter.return_value.first.return_value


def test_delete_item_not_found():
    db = Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    result = delete_item(db, 1)

    db.query.assert_called_once_with(Item)
    db.query.return_value.filter.assert_called_once_with(Item.id == 1)
    assert result is None
```