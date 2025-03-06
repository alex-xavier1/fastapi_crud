# ```python

# This module provides unit tests for the database connection module

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from unittest.mock import patch, MagicMock
from typing import Optional

# Mocked packages
with patch('sqlalchemy.create_engine', return_value=MagicMock()) as mock_create_engine:
    with patch('sqlalchemy.orm.sessionmaker', return_value=MagicMock()) as mock_sessionmaker:
        with patch('sqlalchemy.ext.declarative.declarative_base', return_value=MagicMock()) as mock_declarative_base:
            from database import DATABASE_URL, engine, SessionLocal, Base

def test_database_url():
    assert DATABASE_URL == os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/fastapi_db")

def test_engine_creation():
    mock_create_engine.assert_called_once_with(DATABASE_URL)

def test_session_local_creation():
    mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)

def test_base_creation():
    mock_declarative_base.assert_called_once()

# Test with invalid DATABASE_URL
def test_invalid_database_url():
    with patch.dict(os.environ, {'DATABASE_URL': ''}):
        with pytest.raises(Exception):
            create_engine(DATABASE_URL)

# Test with missing DATABASE_URL
def test_missing_database_url():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(KeyError):
            create_engine(DATABASE_URL)
```