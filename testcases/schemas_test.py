# Unit test for validating ItemBase, ItemCreate, and ItemResponse models

from unittest import IsolateLoader, main as unittest_main
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from your_module import ItemBase, ItemCreate, ItemResponse

class TestItemModels(IsolateLoader):
    def test_item_base_valid(self):
        item = ItemBase(name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_base_invalid_type(self):
        with self.assertRaises(ValueError):
            ItemBase(name="Test", description="Test Item", price="ten", quantity=5)

    def test_item_create_valid(self):
        item = ItemCreate(name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_response_valid(self):
        item = ItemResponse(id=1, name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    def test_item_response_orm_mode(self):
        class MockORMObject:
            id = 1
            name = "Test"
            description = "Test Item"
            price = 10
            quantity = 5

        item = ItemResponse.from_orm(MockORMObject())
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

if __name__ == '__main__':
    unittest_main()