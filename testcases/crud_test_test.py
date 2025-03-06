# Here are the unit tests for the functions mentioned above:


```python
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_items, get_item, create_item, update_item, delete_item
from models import Item
from schemas import ItemCreate
import pytest

client = TestClient(app)

def test_get_items():
    with patch.object(Session, 'query', return_value=MagicMock()):
        items = get_items(Session())
        Session.query.assert_called_once_with(Item)
        assert isinstance(items, MagicMock)

def test_get_item():
    with patch.object(Session, 'query', return_value=MagicMock()):
        item_id = 1
        item = get_item(Session(), item_id)
        Session.query.assert_called_once_with(Item)
        assert isinstance(item, MagicMock)

def test_create_item():
    with patch.object(Session, 'add', return_value=MagicMock()) as mock_add, \
         patch.object(Session, 'commit', return_value=MagicMock()) as mock_commit, \
         patch.object(Session, 'refresh', return_value=MagicMock()) as mock_refresh:

        item_data = ItemCreate(name="testItem", price=100)
        item = create_item(Session(), item_data)

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once()

def test_update_item():
    with patch.object(Session, 'query', return_value=MagicMock()):
        item_id = 1
        item_data = ItemCreate(name="updatedItem", price=200)
        item = update_item(Session(), item_id, item_data)

        Session.query.assert_called_once_with(Item)
        assert isinstance(item, MagicMock)

def test_delete_item():
    with patch.object(Session, 'query', return_value=MagicMock()), \
         patch.object(Session, 'delete', return_value=MagicMock()) as mock_delete, \
         patch.object(Session, 'commit', return_value=MagicMock()) as mock_commit:

        item_id = 1
        item = delete_item(Session(), item_id)

        mock_delete.assert_called_once()
        mock_commit.assert_called_once()
        assert isinstance(item, MagicMock)
```
Please note that these unit tests are quite simple and do not cover all potential edge cases or error handling scenarios. They are designed to test the basic functionality of each function in isolation. For more comprehensive tests, you would need to consider additional scenarios, such