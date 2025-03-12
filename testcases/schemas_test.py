# Unit test for validating the ItemBase, ItemCreate, and ItemResponse models

from unittest import IsolateAsyncioTestCase
from unittest.mock import patch, AsyncMock
from my_module import ItemBase, ItemCreate, ItemResponse

class TestModels(IsolateAsyncioTestCase):
    async def test_item_base_model_valid(self):
        item = ItemBase(name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    async def test_item_create_model_valid(self):
        item = ItemCreate(name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    async def test_item_response_model_valid(self):
        item = ItemResponse(id=1, name="Test", description="Test Item", price=10, quantity=5)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 5)

    async def test_item_base_model_invalid_type(self):
        with self.assertRaises(ValueError):
            ItemBase(name="Test", description="Test Item", price="ten", quantity=5)

    async def test_item_create_model_invalid_type(self):
        with self.assertRaises(ValueError):
            ItemCreate(name="Test", description="Test Item", price="ten", quantity=5)

    async def test_item_response_model_invalid_type(self):
        with self.assertRaises(ValueError):
            ItemResponse(id="one", name="Test", description="Test Item", price=10, quantity=5)