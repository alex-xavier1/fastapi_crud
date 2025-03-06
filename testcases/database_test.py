# ```python

import os
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class TestDatabaseConfig(unittest.TestCase):

    @patch.object(os.environ, 'get', return_value="postgresql://user:password@localhost/fastapi_db")
    def test_database_url(self, mock_get):
        from your_module import DATABASE_URL
        self.assertEqual(DATABASE_URL, "postgresql://user:password@localhost/fastapi_db")

    @patch.object(create_engine, 'return_value')
    @patch.object(os.environ, 'get', return_value="postgresql://user:password@localhost/fastapi_db")
    def test_engine(self, mock_get, mock_create_engine):
        from your_module import engine
        mock_create_engine.assert_called_once_with("postgresql://user:password@localhost/fastapi_db")
        self.assertEqual(engine, mock_create_engine.return_value)

    @patch.object(sessionmaker, 'return_value')
    @patch('your_module.engine', new_callable=MagicMock)
    def test_session_local(self, mock_engine, mock_sessionmaker):
        from your_module import SessionLocal
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=mock_engine)
        self.assertEqual(SessionLocal, mock_sessionmaker.return_value)

    @patch.object(declarative_base, 'return_value')
    def test_base(self, mock_declarative_base):
        from your_module import Base
        mock_declarative_base.assert_called_once()
        self.assertEqual(Base, mock_declarative_base.return_value)

if __name__ == '__main__':
    unittest.main()
```

This testing code verifies the correct setup of the FastAPI database configuration. It tests all the configurations including the DATABASE_URL, engine, SessionLocal, and Base. Mocking is used to isolate the tests from external dependencies.