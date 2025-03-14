# Test database setup and session creation for FastAPI app

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from unittest.mock import MagicMock, patch
import os

from your_module import DATABASE_URL, engine, SessionLocal, Base

@pytest.fixture
def test_engine():
    test_database_url = "sqlite:///:memory:"
    engine = create_engine(test_database_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def test_session(test_engine):
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    yield session
    session.close()

def test_database_url_from_env():
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://test:test@localhost/test_db"}):
        assert DATABASE_URL == "postgresql://test:test@localhost/test_db"

def test_engine_creation(test_engine):
    assert test_engine.url == create_engine("sqlite:///:memory:").url

def test_session_creation(test_session):
    assert isinstance(test_session, sessionmaker)

def test_base_declarative():
    assert isinstance(Base, declarative_base().__class__)