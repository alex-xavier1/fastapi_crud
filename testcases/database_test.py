# Unit tests for database module ensuring proper setup and connection

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from unittest.mock import patch
from my_module import DATABASE_URL, engine, SessionLocal, Base

def test_database_url_from_environment():
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://test_user:test_password@test_host/test_db"}):
        from my_module import DATABASE_URL
        assert DATABASE_URL == "postgresql://test_user:test_password@test_host/test_db"

def test_engine_creation():
    with patch("sqlalchemy.create_engine") as mock_create_engine:
        from my_module import engine
        mock_create_engine.assert_called_once_with(DATABASE_URL)
        assert engine == mock_create_engine.return_value

def test_sessionmaker_creation():
    with patch("sqlalchemy.orm.sessionmaker") as mock_sessionmaker:
        from my_module import SessionLocal
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)
        assert SessionLocal == mock_sessionmaker.return_value

def test_base_declarative():
    from my_module import Base
    assert isinstance(Base, declarative_base().__class__)