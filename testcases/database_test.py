# Test the SQLAlchemy setup for FastAPI

import os
from unittest import TestCase, mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from your_module import DATABASE_URL, engine, SessionLocal, Base

class TestDatabaseSetup(TestCase):
    def setUp(self):
        self.mock_engine = mock.Mock()
        self.mock_sessionmaker = mock.Mock(return_value=mock.Mock())
        self.mock_declarative_base = mock.Mock(return_value=mock.Mock())

    def test_database_url_from_environment(self):
        with mock.patch.dict(os.environ, {"DATABASE_URL": "postgresql://test:test@localhost/test_db"}):
            from your_module import DATABASE_URL
            self.assertEqual(DATABASE_URL, "postgresql://test:test@localhost/test_db")

    @mock.patch("sqlalchemy.create_engine")
    def test_engine_creation(self, mock_create_engine):
        mock_create_engine.return_value = self.mock_engine
        from your_module import engine
        mock_create_engine.assert_called_once_with(DATABASE_URL)
        self.assertEqual(engine, self.mock_engine)

    @mock.patch("sqlalchemy.orm.sessionmaker")
    def test_session_local_creation(self, mock_sessionmaker):
        mock_sessionmaker.return_value = self.mock_sessionmaker
        from your_module import SessionLocal
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)
        self.assertEqual(SessionLocal, self.mock_sessionmaker)

    @mock.patch("sqlalchemy.ext.declarative.declarative_base")
    def test_base_creation(self, mock_declarative_base):
        mock_declarative_base.return_value = self.mock_declarative_base
        from your_module import Base
        mock_declarative_base.assert_called_once()
        self.assertEqual(Base, self.mock_declarative_base)