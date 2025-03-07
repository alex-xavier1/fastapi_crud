# Unit tests for schemas.py

```python
# This test suite verifies the functionality and edge cases of the ItemBase, ItemCreate and ItemResponse models.

import unittest
from unittest.mock import patch
from pydantic import ValidationError
from your_module import ItemBase, ItemCreate, ItemResponse

class TestItemBase(unittest.TestCase):

    def test_create_item_base(self):
        item = ItemBase(name="Test Item", description="Test Description", price=100, quantity=10)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "Test Description")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)

    def test_item_base_validation(self):
        with self.assertRaises(ValidationError):
            item = ItemBase(name="Test Item", description="Test Description", price="invalid", quantity=10)

    def test_item_base_negative_quantity(self):
        with self.assertRaises(ValidationError):
            item = ItemBase(name="Test Item", description="Test Description", price=100, quantity=-10)

class TestItemResponse(unittest.TestCase):

    def test_create_item_response(self):
        item = ItemResponse(id=1, name="Test Item", description="Test Description", price=100, quantity=10)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "Test Description")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)

    def test_item_response_validation(self):
        with self.assertRaises(ValidationError):
            item = ItemResponse(id="invalid", name="Test Item", description="Test Description", price=100, quantity=10)


if __name__ == "__main__":
    unittest.main()
```