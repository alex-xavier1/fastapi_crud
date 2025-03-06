# ```python

import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock
from httpx import AsyncClient
from app.main import app
from app.models import ItemCreate, ItemResponse

@pytest.mark.asyncio
async def test_item_create():
    data = {"name": "Test", "description": "Test item", "price": 100, "quantity": 10}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items/", json=data)
    assert response.status_code == 200
    item = ItemCreate(**response.json())
    assert item.name == "Test"
    assert item.description == "Test item"

@pytest.mark.asyncio
async def test_item_response():
    data = {"id": 1, "name": "Test", "description": "Test item", "price": 100, "quantity": 10}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    assert response.status_code == 200
    item = ItemResponse(**response.json())
    assert item.id == 1
    assert item.name == "Test"
    assert item.description == "Test item"

def test_item_create_validation_error():
    data = {"name": "Test", "description": "Test item", "price": "invalid", "quantity": 10}
    with pytest.raises(ValidationError):
        ItemCreate(**data)

def test_item_response_validation_error():
    data = {"id": "invalid", "name": "Test", "description": "Test item", "price": 100, "quantity": 10}
    with pytest.raises(ValidationError):
        ItemResponse(**data)
```