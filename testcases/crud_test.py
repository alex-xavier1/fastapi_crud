# Unit tests for crud.py

```python
# Test module for item CRUD operations with mocked database session

import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
from your_module import get_items, get_item, create_item, update_item, delete_item

class TestItemCRUD(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock(spec=Session)
        self.item_data = ItemCreate(name="Test Item", description="Test Description", price=10.0)
        self.item_id = 1

    @patch('your_module.Session', autospec=True)
    def test_get_items(self, SessionMock):
        SessionMock.return_value = self.db_mock
        items = get_items(self.db_mock)
        self.db_mock.query.return_value.all.assert_called_once()
        self.assertEqual(items, self.db_mock.query.return_value.all.return_value)

    @patch('your_module.Session', autospec=True)
    def test_get_item(self, SessionMock):
        SessionMock.return_value = self.db_mock
        self.db_mock.query.return_value.filter.return_value.first.return_value = Item(id=self.item_id, **self.item_data.dict())
        item = get_item(self.db_mock, self.item_id)
        self.db_mock.query.return_value.filter.assert_called_once_with(Item.id == self.item_id)
        self.assertEqual(item.id, self.item_id)

    @patch('your_module.Session', autospec=True)
    def test_create_item(self, SessionMock):
        SessionMock.return_value = self.db_mock
        new_item = create_item(self.db_mock, self.item_data)
        self.db_mock.add.assert_called_once()
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(new_item)
        self.assertEqual(new_item.name, self.item_data.name)

    @patch('your_module.Session', autospec=True)
    def test_update_item(self, SessionMock):
        SessionMock.return_value = self.db_mock
        self.db_mock.query.return_value.filter.return_value.first.return_value = Item(id=self.item_id, **self.item_data.dict())
        updated_item = update_item(self.db_mock, self.item_id, ItemCreate(name="Updated Item"))
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(updated_item)
        self.assertEqual(updated_item.name, "Updated Item")

    @patch('your_module.Session', autospec=True)
    def test_delete_item(self, SessionMock):
        SessionMock.return_value = self.db_mock
        self.db_mock.query.return_value.filter.return_value.first.return_value = Item(id=self.item_id, **self.item_data.dict())
        deleted_item = delete_item(self.db_mock, self.item_id)
        self.db_mock.delete.assert_called_once_with(deleted_item)
        self.db_mock.commit.assert_called_once()
        self.assertEqual(deleted_item.id, self.item_id)

if __name__ == '__main__':
    unittest.main()
```