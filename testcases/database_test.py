# Unit tests for database.py

```python
# Unit test to verify the database connection and session creation

import unittest
from unittest.mock import patch, MagicMock
from your_module import engine, SessionLocal, Base

class TestDatabaseModule(unittest.TestCase):
    @patch('sqlalchemy.create_engine')
    def test_engine_creation(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        self.assertEqual(engine, mock_engine)

    @patch('sqlalchemy.orm.sessionmaker')
    def test_session_creation(self, mock_sessionmaker):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        self.assertEqual(SessionLocal, mock_session)

    @patch('sqlalchemy.ext.declarative.declarative_base')
    def test_base_creation(self, mock_declarative_base):
        mock_base = MagicMock()
        mock_declarative_base.return_value = mock_base
        self.assertEqual(Base, mock_base)

if __name__ == '__main__':
    unittest.main()
```