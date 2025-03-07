# Unit tests for routes.py

```python
# This is a unit test module for testing CRUD operations in the FastAPI router module
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch
from database import SessionLocal
import crud, schemas
import main

def test_read_items():
    with patch.object(crud, 'get_items') as mock_get_items:
        mock_get_items.return_value = [{'name': 'item1', 'description': 'description', 'price': 100}]
        result = main.read_items(Mock(spec=Session))
        assert result == [{'name': 'item1', 'description': 'description', 'price': 100}]

def test_read_item_success():
    with patch.object(crud, 'get_item') as mock_get_item:
        mock_get_item.return_value = {'name': 'item1', 'description': 'description', 'price': 100}
        result = main.read_item(1, Mock(spec=Session))
        assert result == {'name': 'item1', 'description': 'description', 'price': 100}

def test_read_item_failure():
    with patch.object(crud, 'get_item') as mock_get_item:
        mock_get_item.return_value = None
        with pytest.raises(HTTPException):
            main.read_item(1, Mock(spec=Session))

def test_create_item():
    with patch.object(crud, 'create_item') as mock_create_item:
        mock_create_item.return_value = {'name': 'item1', 'description': 'description', 'price': 100}
        result = main.create_item({'name': 'item1', 'description': 'description', 'price': 100}, Mock(spec=Session))
        assert result == {'name': 'item1', 'description': 'description', 'price': 100}

def test_update_item_success():
    with patch.object(crud, 'update_item') as mock_update_item:
        mock_update_item.return_value = {'name': 'item1', 'description': 'description', 'price': 100}
        result = main.update_item(1, {'name': 'item1', 'description': 'description', 'price': 100}, Mock(spec=Session))
        assert result == {'name': 'item1', 'description': 'description', 'price': 100}

def test_update_item_failure():
    with patch.object(crud, 'update_item') as mock_update_item:
        mock_update_item.return_value = None
        with pytest.raises(HTTPException):
            main.update_item(1, {'name': 'item1', 'description': 'description', 'price': 100}, Mock(spec=Session))

def test_delete_item_success():
    with patch.object(crud, 'delete_item') as mock_delete_item:
        mock_delete_item.return_value = {'detail': 'Item deleted'}
        result = main.delete_item(1, Mock(spec=Session))
        assert result == {'detail': 'Item deleted'}

def test_delete_item_failure():
    with patch.object(crud, 'delete_item') as mock_delete_item:
        mock_delete_item.return_value = None
        with pytest.raises(HTTPException):
            main.delete_item(1, Mock(spec=Session))
```