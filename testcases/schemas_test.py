# Unit test to verify the validation and serialization of Item models in a FastAPI application

from unittest import IsolateTestCase
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from pydantic import ValidationError
from your_module import ItemBase, ItemCreate, ItemResponse

class TestItemModels(IsolateTestCase):
    def test_item_base_valid(self):
        item = ItemBase(name="Test Item", description="A test item", price=10, quantity=5)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_base_invalid_type(self):
        with self.assertRaises(ValidationError):
            ItemBase(name="Test Item", description="A test item", price="ten", quantity=5)

    def test_item_create_valid(self):
        item = ItemCreate(name="Test Item", description="A test item", price=10, quantity=5)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_response_valid(self):
        item = ItemResponse(id=1, name="Test Item", description="A test item", price=10, quantity=5)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_response_orm_mode(self):
        orm_item = MagicMock()
        orm_item.id = 1
        orm_item.name = "Test Item"
        orm_item.description = "A test item"
        orm_item.price = 10
        orm_item.quantity = 5
        item = ItemResponse.from_orm(orm_item)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)