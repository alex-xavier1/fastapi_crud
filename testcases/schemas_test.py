# Unit tests for schemas.py

```python
# This file contains unit tests for the ItemBase, ItemCreate, and ItemResponse classes in the module.

import unittest
from unittest.mock import patch
from pydantic import ValidationError
from module import ItemBase, ItemCreate, ItemResponse

class TestItemBase(unittest.TestCase):
    def test_create_item_base(self):
        item = ItemBase(name="TestItem", description="This is a test item", price=100, quantity=2)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 2)

    def test_item_base_validation(self):
        with self.assertRaises(ValidationError):
            item = ItemBase(name="TestItem", description="This is a test item", price="invalid_price", quantity=2)

    def test_item_base_boundaries(self):
        with self.assertRaises(ValidationError):
            item = ItemBase(name="TestItem", description="This is a test item", price=-1, quantity=0)

class TestItemCreate(unittest.TestCase):
    def test_create_item_create(self):
        item = ItemCreate(name="TestItem", description="This is a test item", price=100, quantity=2)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 2)

class TestItemResponse(unittest.TestCase):
    def test_create_item_response(self):
        item = ItemResponse(name="TestItem", description="This is a test item", price=100, quantity=2, id=1)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.id, 1)

if __name__ == '__main__':
    unittest.main()
```
In this script, we're testing the ItemBase, ItemCreate and ItemResponse classes from the module. We create instances of these classes and check that the values have been assigned correctly. We also test the data validation provided by Pydantic by trying to create an item with an invalid price (a string instead of an integer), and an item with boundary values for the price and quantity fields.