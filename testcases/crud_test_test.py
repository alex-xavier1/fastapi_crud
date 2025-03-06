# ```python

from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_items, get_item, create_item, update_item, delete_item
from models import Item
from schemas import ItemCreate

client = TestClient(app)

def test_get_items():
    with patch.object(Session, 'query', return_value=Mock(all=Mock(return_value=[]))) as mock:
        response = get_items(db=Mock())
        mock.assert_called_once_with(Item)
        assert response == []

def test_get_item():
    with patch.object(Session, 'query', return_value=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None))))) as mock:
        response = get_item(db=Mock(), item_id=1)
        mock.assert_called_once_with(Item)
        assert response == None

def test_create_item():
    with patch.object(Session, 'add') as mock_add:
        with patch.object(Session, 'commit') as mock_commit:
            with patch.object(Session, 'refresh') as mock_refresh:
                item = ItemCreate(name="test_name", description="test_description", price=10)
                response = create_item(db=Mock(), item=item)
                mock_add.assert_called_once()
                mock_commit.assert_called_once()
                mock_refresh.assert_called_once()
                assert response == item

def test_update_item():
    with patch.object(Session, 'query', return_value=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=Item()))))) as mock_query:
        with patch.object(Session, 'commit') as mock_commit:
            with patch.object(Session, 'refresh') as mock_refresh:
                item = ItemCreate(name="test_name", description="test_description", price=10)
                response = update_item(db=Mock(), item_id=1, item=item)
                mock_query.assert_called_once_with(Item)
                mock_commit.assert_called_once()
                mock_refresh.assert_called_once()
                assert isinstance(response, Item)

def test_delete_item():
    with patch.object(Session, 'query', return_value=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=Item()))))) as mock_query:
        with patch.object(Session, 'delete') as mock_delete:
            with patch.object(Session, 'commit') as mock_commit:
                response = delete_item(db=Mock(), item_id=1)
                mock_query.assert_called_once_with(Item)
                mock_delete.assert