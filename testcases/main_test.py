# ```python

# Test FastAPI application initialization and routes.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import Mock, patch
from main import app
from models import Base

# Mocking Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mocking Base Model
Base.metadata.create_all(bind=engine)

# Client for Testing
client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Mocking the Dependencies
app.dependency_overrides[get_db] = override_get_db


@patch('routes.router')
def test_app_initialization(mock_router):
    response = client.get('/')
    assert response.status_code == 200
    mock_router.assert_called_once()


@patch('models.Base')
def test_database_initialization(mock_base):
    mock_base.metadata.create_all.assert_called_once_with(bind=engine)


@patch('fastapi.FastAPI.include_router')
def test_include_router(mock_include_router):
    mock_include_router.assert_called_once_with(router)
    

@patch('fastapi.FastAPI')
def test_create_app(mock_app):
    assert isinstance(app, FastAPI)
    mock_app.assert_called_once()
```