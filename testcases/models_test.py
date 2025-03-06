# ```python

# Unit tests for the Item and Task models in the FastAPI application.
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, Item, Task

# Mocking database connection
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_item_model():
    # Mocking a SessionLocal
    with TestingSessionLocal() as db:
        # Testing normal case
        test_item = Item(id=1, name="Test Item", description="A test item", price=100, quantity=5)
        db.add(test_item)
        db.commit()
        db.refresh(test_item)
        assert test_item.id == 1
        assert test_item.name == "Test Item"
        assert test_item.description == "A test item"
        assert test_item.price == 100
        assert test_item.quantity == 5

        # Testing edge case with null values
        try:
            test_item2 = Item(id=2, name=None, description=None, price=None, quantity=None)
            db.add(test_item2)
            db.commit()
            db.refresh(test_item2)
        except Exception as e:
            assert isinstance(e, TypeError)

def test_task_model():
    # Mocking a SessionLocal
    with TestingSessionLocal() as db:
        # Testing normal case
        test_task = Task(id=1, name="Test Task")
        db.add(test_task)
        db.commit()
        db.refresh(test_task)
        assert test_task.id == 1
        assert test_task.name == "Test Task"

        # Testing edge case with null values
        try:
            test_task2 = Task(id=2, name=None)
            db.add(test_task2)
            db.commit()
            db.refresh(test_task2)
        except Exception as e:
            assert isinstance(e, TypeError)
```