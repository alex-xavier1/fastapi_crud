# Unit tests for database.py

```python
# Unit tests for SQLAlchemy database configuration module

import os
import unittest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from your_module import DATABASE_URL, engine, SessionLocal, Base

class TestDatabaseConfig(unittest.TestCase):

    @patch('os.environ.get')
    def test_database_url(self, mock_env):
        mock_env.return_value = 'mock_database_url'
        self.assertEqual(DATABASE_URL, 'mock_database_url')
        mock_env.assert_called_once_with('DATABASE_URL', 'postgresql://user:password@localhost/fastapi_db')

    @patch('sqlalchemy.create_engine')
    def test_engine_creation(self, mock_create_engine):
        mock_create_engine.return_value = 'mock_engine'
        self.assertEqual(engine, 'mock_engine')
        mock_create_engine.assert_called_once_with(DATABASE_URL)

    @patch('sqlalchemy.orm.sessionmaker')
    def test_session_local(self, mock_sessionmaker):
        mock_sessionmaker.return_value = 'mock_session'
        self.assertEqual(SessionLocal, 'mock_session')
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)

    @patch('sqlalchemy.ext.declarative.declarative_base')
    def test_base_declaration(self, mock_base):
        mock_base.return_value = 'mock_base'
        self.assertEqual(Base, 'mock_base')
        mock_base.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

This unit test module tests the database configuration by mocking the external dependencies and checking if they are called with the correct arguments. It validates the `DATABASE_URL`, `engine`, `SessionLocal`, and `Base` variables. The module follows the best practices for Flask testing, covers edge cases of function calls, and ensures test readability and maintainability.