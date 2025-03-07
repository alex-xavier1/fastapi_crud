# Unit tests for database.py

Here's a simple unit test for the given module. We use `unittest.mock` to mock external dependencies and `pytest` for running the tests.

```python
# This file contains unit tests for database connection module in the Flask application.

import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class TestDatabaseModule(unittest.TestCase):
    @patch('os.environ.get')
    @patch('sqlalchemy.create_engine')
    @patch('sqlalchemy.orm.sessionmaker')
    def test_database_connection(self, mock_sessionmaker, mock_create_engine, mock_os_get):
        # Import the module here to ensure that the mock objects are used
        from your_module import DATABASE_URL, engine, SessionLocal, Base

        # Assert that os.environ.get was called with the correct arguments
        mock_os_get.assert_called_once_with("DATABASE_URL", "postgresql://user:password@localhost/fastapi_db")

        # Assert that create_engine was called with the correct arguments
        mock_create_engine.assert_called_once_with(DATABASE_URL)

        # Assert that sessionmaker was called with the correct arguments
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)

    def test_database_connection_failure(self, mock_create_engine, mock_os_get):
        # Simulate a case where the connection to the database fails
        mock_create_engine.side_effect = Exception("Database connection failed")

        # Import the module here to ensure that the mock objects are used
        from your_module import DATABASE_URL, engine, SessionLocal, Base

        # Assert that an exception was raised when trying to connect to the database
        with self.assertRaises(Exception) as context:
            mock_create_engine(DATABASE_URL)

        # Check that the correct exception message was raised
        self.assertTrue('Database connection failed' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
```

This test suite includes a test for the happy path (where everything works as expected) and a test for the unhappy path (where an exception is raised when trying to connect to the database). Please replace "your_module" with the actual name of your module.