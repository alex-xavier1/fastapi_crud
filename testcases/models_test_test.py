# ```python

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from your_module import Item, Task
from unittest.mock import Mock, patch

# setup a mock database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# test the Item model
def test_item_model(test_db: Session):
    new_item = Item(id=1, name="Test item", description="Test description", price=50, quantity=5)
    test_db.add(new_item)
    test_db.commit()
    db_item = test_db.query(Item).filter_by(name="Test item").first()
    assert db_item.name == "Test item"

# test the Item model with incorrect data
def test_item_model_incorrect_data(test_db: Session):
    with pytest.raises(Exception):
        new_item = Item(id="one", name="Test item", description="Test description", price="fifty", quantity="five")
        test_db.add(new_item)
        test_db.commit()

# test the Task model
def test_task_model(test_db: Session):
    new_task = Task(id=1, name="Test task")
    test_db.add(new_task)
    test_db.commit()
    db_task = test_db.query(Task).filter_by(name="Test task").first()
    assert db_task.name == "Test task"

# test the Task model with incorrect data
def test_task_model_incorrect_data(test_db: Session):
    with pytest.raises(Exception):
        new_task = Task(id="one", name="Test task")
        test_db.add(new_task)
        test_db.commit()
```

This test script does the following:
- Creates a mock database session for testing.
- Tests the Item and Task models by adding an instance and checking if it can be retrieved from the database.
- Tests edge cases by trying to add an instance with incorrect data types to the database, which should raise an exception.

Note: Make sure to replace "your_module" with the actual name of your python module where the `Item` and `Task` classes are defined.