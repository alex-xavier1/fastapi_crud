# Unit tests for schemas.py

```python
# This file contains unit tests for the ItemBase, ItemCreate and ItemResponse classes in Flask using Pydantic BaseModel

import unittest
from unittest.mock import patch
from pydantic import ValidationError
from main import ItemBase, ItemCreate, ItemResponse

class TestItemBase(unittest.TestCase):

    def test_item_base_model(self):
        item = ItemBase(name="TestItem", description="TestDescription", price=100, quantity=10)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "TestDescription")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)

    def test_item_base_model_invalid_data(self):
        with self.assertRaises(ValidationError):
            ItemBase(name="TestItem", description="TestDescription", price="invalid", quantity=10)

class TestItemCreate(unittest.TestCase):

    def test_item_create_model(self):
        item = ItemCreate(name="TestItem", description="TestDescription", price=100, quantity=10)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "TestDescription")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)

    def test_item_create_model_invalid_data(self):
        with self.assertRaises(ValidationError):
            ItemCreate(name="TestItem", description="TestDescription", price="invalid", quantity=10)

class TestItemResponse(unittest.TestCase):

    def test_item_response_model(self):
        item = ItemResponse(name="TestItem", description="TestDescription", price=100, quantity=10, id=1)
        self.assertEqual(item.name, "TestItem")
        self.assertEqual(item.description, "TestDescription")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.id, 1)

    def test_item_response_model_invalid_data(self):
        with self.assertRaises(ValidationError):
            ItemResponse(name="TestItem", description="TestDescription", price="invalid", quantity=10, id=1)

if __name__ == "__main__":
    unittest.main()
```

This test suite creates unit tests for the models `ItemBase`, `ItemCreate`, and `ItemResponse`. It validates their normal functionality by initializing them with valid data and checking if the values are correctly set. It also tests edge cases by trying to initialize them with invalid data types, expecting a `ValidationError` to be raised.