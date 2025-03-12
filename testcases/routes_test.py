# Unit tests for routes.py

```python
# Unit tests for the items module ensuring correct behavior and error handling

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, crud, schemas
from sqlalchemy.orm import Session

client = TestClient(app)

def fake_get_db():
    db = MagicMock(spec=Session)
    yield db
    db.close.assert_called_once()

@patch("main.crud.get_items", return_value=[schemas.ItemResponse(id=1, name="item1", description="desc1")])
def test_read_items(mock_get_items):
    response = client.get("/items", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    mock_get_items.assert_called_once()

@patch("main.crud.get_item", return_value=schemas.ItemResponse(id=1, name="item1", description="desc1"))
def test_read_item(mock_get_item):
    response = client.get("/items/1", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    mock_get_item.assert_called_once_with(mock_get_item.call_args.args[0], 1)

@patch("main.crud.get_item", return_value=None)
def test_read_item_not_found(mock_get_item):
    response = client.get("/items/1", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@patch("main.crud.create_item", return_value=schemas.ItemResponse(id=1, name="new_item", description="new_desc"))
def test_create_item(mock_create_item):
    response = client.post("/items", json={"name": "new_item", "description": "new_desc"}, headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 201
    mock_create_item.assert_called_once()

@patch("main.crud.update_item", return_value=schemas.ItemResponse(id=1, name="updated_item", description="updated_desc"))
def test_update_item(mock_update_item):
    response = client.put("/items/1", json={"name": "updated_item", "description": "updated_desc"}, headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    mock_update_item.assert_called_once_with(mock_update_item.call_args.args[0], 1, mock_update_item.call_args.args[2])

@patch("main.crud.update_item", return_value=None)
def test_update_item_not_found(mock_update_item):
    response = client.put("/items/1", json={"name": "updated_item", "description": "updated_desc"}, headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@patch("main.crud.delete_item", return_value=schemas.ItemResponse(id=1, name="item1", description="desc1"))
def test_delete_item(mock_delete_item):
    response = client.delete("/items/1", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Item deleted"}

@patch("main.crud.delete_item", return_value=None)
def test_delete_item_not_found(mock_delete_item):
    response = client.delete("/items/1", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
```