# Unit tests for schemas.py

```python
# Unit tests for validating the behavior of ItemBase, ItemCreate, and ItemResponse models.

from unittest import TestCase, mock
from your_module import ItemBase, ItemCreate, ItemResponse

class TestItemModels(TestCase):
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

    def test_item_response_invalid_type(self):
        with self.assertRaises(ValueError):
            ItemResponse(id="one", name="Test", description="Test Item", price=10, quantity=5)
```