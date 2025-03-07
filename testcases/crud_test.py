# Unit tests for crud.py

```python
# Unit tests for CRUD operations on Item model in Flask application using SQLAlchemy ORM
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
from main import get_items, get_item, create_item, update_item, delete_item

@patch('main.Session')
def test_get_items(mock_session):
    # Mock the return value of query.all()
    mock_session.query.return_value.all.return_value = ['item1', 'item2']
    result = get_items(mock_session)
    assert result == ['item1', 'item2']

@patch('main.Session')
def test_get_item(mock_session):
    # Mock the return value of query.filter().first()
    mock_session.query.return_value.filter.return_value.first.return_value = 'item1'
    result = get_item(mock_session, 1)
    assert result == 'item1'

@patch('main.Session')
def test_create_item(mock_session):
    # Mock the return value of item creation and commit
    mock_item = MagicMock(spec=ItemCreate)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    result = create_item(mock_session, mock_item)
    assert isinstance(result, Item)

@patch('main.Session')
def test_update_item(mock_session):
    # Mock the return value of item update and commit
    mock_item = MagicMock(spec=ItemCreate)
    mock_session.query.return_value.filter.return_value.first.return_value = mock_item
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    result = update_item(mock_session, 1, mock_item)
    assert isinstance(result, Item)

@patch('main.Session')
def test_delete_item(mock_session):
    # Mock the return value of item deletion and commit
    mock_session.query.return_value.filter.return_value.first.return_value = 'item1'
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    result = delete_item(mock_session, 1)
    assert result == 'item1'
```