# ```python

from unittest import TestCase
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from pydantic import ValidationError
from main import app, ItemBase, ItemCreate, ItemResponse

client = TestClient(app)


class TestItemBase(TestCase):

    def test_item_base(self):
        with self.assertRaises(ValidationError):
            ItemBase(name="Item1", description="Test Item", price="string", quantity=10)
        with self.assertRaises(ValidationError):
            ItemBase(name="Item1", description="Test Item", price=10, quantity="string")
        with self.assertRaises(ValidationError):
            ItemBase(name=123, description="Test Item", price=10, quantity=10)
        with self.assertRaises(ValidationError):
            ItemBase(name="Item1", description=123, price=10, quantity=10)

        item = ItemBase(name="Item1", description="Test Item", price=10, quantity=10)
        self.assertEqual(item.name, "Item1")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 10)


class TestItemCreate(TestCase):

    def test_item_create(self):
        with self.assertRaises(ValidationError):
            ItemCreate(name="Item1", description="Test Item", price="string", quantity=10)
        with self.assertRaises(ValidationError):
            ItemCreate(name="Item1", description="Test Item", price=10, quantity="string")
        with self.assertRaises(ValidationError):
            ItemCreate(name=123, description="Test Item", price=10, quantity=10)
        with self.assertRaises(ValidationError):
            ItemCreate(name="Item1", description=123, price=10, quantity=10)

        item = ItemCreate(name="Item1", description="Test Item", price=10, quantity=10)
        self.assertEqual(item.name, "Item1")
        self.assertEqual(item.description, "Test Item")
        self.assertEqual(item.price, 10)
        self.assertEqual(item.quantity, 10)


class TestItemResponse(TestCase):

    def test_item_response(self):
        with self.assertRaises(ValidationError):
            ItemResponse(name="Item1", description="Test Item", price=10, quantity=10, id="string")
        with self.assertRaises(ValidationError):
            ItemResponse(name=123, description="Test Item", price=10, quantity=10, id=1)
        with self.assertRaises