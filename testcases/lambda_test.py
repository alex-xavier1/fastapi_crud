# ```python

import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from your_module import app  # Replace with the actual name of your module

@pytest.mark.asyncio
async def test_get_open_prs():
    with patch('your_module.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"number": 1, "title": "PR 1"},
            {"number": 2, "title": "PR 2"}
        ]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/get_open_prs/test/test")  # Assuming you have a route defined for this function

        assert response.status_code == 200
        assert response.json() == [
            {"number": 1, "title": "PR 1"},
            {"number": 2, "title": "PR 2"}
        ]


@pytest.mark.asyncio
async def test_get_open_prs_no_prs():
    with patch('your_module.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/get_open_prs/test/test")

        assert response.status_code == 200
        assert response.json() == []

@pytest.mark.asyncio
async def test_get_open_prs_error():
    with patch('your_module.requests.get') as mock_get:
        mock_get.return_value.status_code = 500

        async with AsyncClient(app=app, base_url="http://test") as ac:
            with pytest.raises(HTTPException):
                await ac.get("/get_open_prs/test/test")

@pytest.mark.asyncio
async def test_get_pr_changed_files():
    with patch('your_module.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"filename": "test.py"}
        ]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/get_pr_changed_files/test/test/1")  # Assuming you have a route defined for this function

        assert response.status_code == 200
        assert response.json() == [
            {"filename": "test.py"}
        ]

# Continue creating tests for the remaining functions following the similar pattern.

```