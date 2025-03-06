# ```python

import pytest
from fastapi.testclient import TestClient
from main import app, ItemCreate, ItemResponse
from mock import patch
from pydantic import ValidationError

client = TestClient(app)

def test_item_create_success():
    item_data = {'name': 'Test Item', 'description': 'This is a test item', 'price': 100, 'quantity': 10}
    response = client.post('/items/', json=item_data)
    assert response.status_code == 200
    assert response.json() == {'name': 'Test Item', 'description': 'This is a test item', 'price': 100, 'quantity': 10}

@patch('main.ItemCreate')
def test_item_create_validation_error(mock_item_create):
    mock_item_create.side_effect = ValidationError
    item_data = {'name': 'Test Item', 'description': 'This is a test item', 'price': '100', 'quantity': 10}
    response = client.post('/items/', json=item_data)
    assert response.status_code == 422

def test_item_create_missing_field():
    item_data = {'description': 'This is a test item', 'price': 100, 'quantity': 10}
    response = client.post('/items/', json=item_data)
    assert response.status_code == 422

def test_item_create_negative_price():
    item_data = {'name': 'Test Item', 'description': 'This is a test item', 'price': -100, 'quantity': 10}
    response = client.post('/items/', json=item_data)
    assert response.status_code == 422

def test_item_create_negative_quantity():
    item_data = {'name': 'Test Item', 'description': 'This is a test item', 'price': 100, 'quantity': -10}
    response = client.post('/items/', json=item_data)
    assert response.status_code == 422

def test_item_response_success():
    item_data = {'id': 1, 'name': 'Test Item', 'description': 'This is a test item', 'price': 100, 'quantity': 10}
    response = client.get('/items/1')
    assert response.status_code == 200
    assert response.json() == item_data

@patch('main.ItemResponse')
def test_item_response_not_found(mock_item_response):
    mock_item_response.side_effect = KeyError
    response = client.get('/items/999')
    assert response.status_code == 404
```