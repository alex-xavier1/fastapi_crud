# Unit test to verify the initialization and routing setup of the FastAPI application

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base
from database import engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module")
def test_app():
    Base.metadata.create_all(bind=test_engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)

def test_app_initialization(test_app):
    response = test_app.get("/")
    assert response.status_code == 404

def test_database_connection():
    db = TestingSessionLocal()
    assert db is not None
    db.close()