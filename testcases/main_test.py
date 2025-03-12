# Unit tests for main.py

```python
# Unit tests for FastAPI application initialization and database setup

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, Base, engine
import pytest

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_app_initialization(client):
    assert app.title == "FastAPI application"

@patch('main.Base.metadata.create_all')
def test_database_tables_creation(mock_create_all):
    mock_create_all.assert_called_once_with(bind=engine)

@patch('main.app.include_router')
def test_routes_inclusion(mock_include_router):
    mock_include_router.assert_called_once_with(router)
```