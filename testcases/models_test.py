# Unit tests for models.py

Here is a sample unit test for the above module. It is assumed that we have a Flask application named `app` and a `db` object from SQLAlchemy.

```
# This is a unit test file for testing the Item and Task models in our Flask application.

import unittest
from unittest.mock import patch
from flask_sqlalchemy import SQLAlchemy
from your_flask_app import app
from your_flask_app.models import Item, Task

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.db = SQLAlchemy(self.app)
    
    def test_item_model(self):
        item = Item(id=1, name='Test Item', description='Test Description', price=100, quantity=10)
        
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.description, 'Test Description')
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 10)

    def test_task_model(self):
        task = Task(id=1, name='Test Task')
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.name, 'Test Task')

    @patch('your_flask_app.models.db.session.add')
    @patch('your_flask_app.models.db.session.commit')
    def test_create_item(self, mock_commit, mock_add):
        item = Item(id=1, name='Test Item', description='Test Description', price=100, quantity=10)
        
        self.db.session.add(item)
        self.db.session.commit()

        mock_add.assert_called_once_with(item)
        mock_commit.assert_called_once()

    @patch('your_flask_app.models.db.session.add')
    @patch('your_flask_app.models.db.session.commit')
    def test_create_task(self, mock_commit, mock_add):
        task = Task(id=1, name='Test Task')
        
        self.db.session.add(task)
        self.db.session.commit()

        mock_add.assert_called_once_with(task)
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()

```

This unittest file creates a new SQLite in-memory database for each test run, tests the creation of `Item` and `Task` objects, and then tests the `create` operations for these objects. Since these operations involve database interactions, we need to mock the `db.session.add` and `db.session.commit` calls to ensure that the tests do not actually commit to the database.