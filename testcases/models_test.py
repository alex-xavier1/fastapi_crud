# from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from main import app
from models import Item, Task
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch('sqlalchemy.orm.Session')
def test_get_item(mock_session):
    mock_item = Item(id=1, name='Test item', description='Test description', price=100, quantity=5)
    mock_session.query.return_value.filter.return_value.first.return_value = mock_item
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Test item', 'description': 'Test description', 'price': 100, 'quantity': 5}

@patch('sqlalchemy.orm.Session')
def test_get_item_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/items/1")
    assert response.status_code == 404

@patch('sqlalchemy.orm.Session')
def test_create_item(mock_session):
    mock_item = Item(id=1, name='Test item', description='Test description', price=100, quantity=5)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    response = client.post("/items/", json={'name': 'Test item', 'description': 'Test description', 'price': 100, 'quantity': 5})
    assert response.status_code == 201
    assert response.json() == {'id': 1, 'name': 'Test item', 'description': 'Test description', 'price': 100, 'quantity': 5}

@patch('sqlalchemy.orm.Session')
def test_get_task(mock_session):
    mock_task = Task(id=1, name='Test task')
    mock_session.query.return_value.filter.return_value.first.return_value = mock_task
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Test task'}

@patch('sqlalchemy.orm.Session')
def test_get_task_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/tasks/1")
    assert response.status_code == 404

@patch('sqlalchemy.orm.Session')
def test_create_task(mock_session):
    mock_task = Task(id=1, name='Test task')
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    response = client.post("/tasks/", json={'name': 'Test task'})
    assert response.status_code == 201
    assert response.json() == {'id': 1, 'name': 'Test task'}