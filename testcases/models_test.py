# ```python
# Unit tests for the Item and Task models in FastAPI

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import Mock, patch

from your_module import Item, Task, Base

# Set up test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Mocking the sessionmaker for the tests
@patch('your_module.SessionLocal', new=TestingSessionLocal)
def test_item_model():
    # Arrange
    session = TestingSessionLocal()
    test_item = Item(id=1, name="Test", description="Test item", price=10, quantity=5)
    
    # Act
    session.add(test_item)
    session.commit()
    session.refresh(test_item)
    
    # Assert
    assert test_item.id == 1
    assert test_item.name == "Test"
    assert test_item.description == "Test item"
    assert test_item.price == 10
    assert test_item.quantity == 5

# Mocking the sessionmaker for the tests
@patch('your_module.SessionLocal', new=TestingSessionLocal)
def test_task_model():
    # Arrange
    session = TestingSessionLocal()
    test_task = Task(id=1, name="Test task")
    
    # Act
    session.add(test_task)
    session.commit()
    session.refresh(test_task)
    
    # Assert
    assert test_task.id == 1
    assert test_task.name == "Test task"

# Cleanup test database after tests
def teardown_module(module):
    TestingSessionLocal.close_all()
    Base.metadata.drop_all(bind=engine)
```