# Unit tests for models.py

```python
# This module contains unit tests for the Item and Task models

import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_project.models import Item, Task, Base

class ModelsTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    @patch('your_project.models.Item')
    def test_create_item(self, MockItem):
        item = MockItem.return_value
        item.name = "Test Item"
        item.description = "Test Description"
        item.price = 10
        item.quantity = 5
        self.session.add(item)
        self.session.commit()
        self.assertEqual(self.session.query(Item).count(), 1)

    @patch('your_project.models.Item')
    def test_item_border_values(self, MockItem):
        item = MockItem.return_value
        item.name = "Test Item"
        item.description = "Test Description"
        item.price = 0
        item.quantity = 0
        self.session.add(item)
        self.session.commit()
        self.assertEqual(self.session.query(Item).count(), 1)

    @patch('your_project.models.Task')
    def test_create_task(self, MockTask):
        task = MockTask.return_value
        task.name = "Test Task"
        self.session.add(task)
        self.session.commit()
        self.assertEqual(self.session.query(Task).count(), 1)

    def tearDown(self):
        self.session.close()

if __name__ == '__main__':
    unittest.main()
```
This test suite includes unit tests for the Item and Task models. The `setUp` method sets up a SQLite database in memory for each test. Instead of interacting with a real database, we use the `unittest.mock.patch()` function to replace the actual `Item` and `Task` models with mock objects. This allows us to isolate the behavior of the code under test from its dependencies. The `test_create_item`, `test_item_border_values` and `test_create_task` methods test the creation of Item and Task objects. The `tearDown` method closes the database session after each test.