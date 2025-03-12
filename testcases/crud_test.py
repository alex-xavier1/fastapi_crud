# Unit tests for CRUD operations on items

from unittest import TestCase, mock
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate
from your_module import get_items, get_item, create_item, update_item, delete_item

class TestItemCRUD(TestCase):
    @mock.patch('your_module.Session')
    def test_get_items(self, MockSession):
        db = MockSession.return_value
        db.query.return_value.all.return_value = [Item(id=1, name="item1"), Item(id=2, name="item2")]
        items = get_items(db)
        self.assertEqual(len(items), 2)

    @mock.patch('your_module.Session')
    def test_get_item(self, MockSession):
        db = MockSession.return_value
        db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="item1")
        item = get_item(db, 1)
        self.assertEqual(item.id, 1)

    @mock.patch('your_module.Session')
    def test_create_item(self, MockSession):
        db = MockSession.return_value
        item_create = ItemCreate(name="new_item")
        db.query.return_value.filter.return_value.first.return_value = None
        new_item = create_item(db, item_create)
        self.assertEqual(new_item.name, "new_item")

    @mock.patch('your_module.Session')
    def test_update_item(self, MockSession):
        db = MockSession.return_value
        db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="item1")
        item_update = ItemCreate(name="updated_item")
        updated_item = update_item(db, 1, item_update)
        self.assertEqual(updated_item.name, "updated_item")

    @mock.patch('your_module.Session')
    def test_delete_item(self, MockSession):
        db = MockSession.return_value
        db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="item1")
        deleted_item = delete_item(db, 1)
        self.assertIsNotNone(deleted_item)