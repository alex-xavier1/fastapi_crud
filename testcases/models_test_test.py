# ```python

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from your_module import Base, Item, Task  # Replace your_module with the actual module name

# Create a mock database for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    return next(get_db())

# Unit test for Item model
def test_item_model(db: Session):
    item = Item(name='Test item', description='This is a test item', price=10, quantity=5)
    db.add(item)
    db.commit()
    db.refresh(item)
    assert item.id == 1
    assert item.name == 'Test item'
    assert item.description == 'This is a test item'
    assert item.price == 10
    assert item.quantity == 5

    # Test for IntegrityError
    with pytest.raises(IntegrityError):
        wrong_item = Item(name=None, description='This is a wrong item', price=10, quantity=5)
        db.add(wrong_item)
        db.commit()

# Unit test for Task model
def test_task_model(db: Session):
    task = Task(name='Test task')
    db.add(task)
    db.commit()
    db.refresh(task)
    assert task.id == 1
    assert task.name == 'Test task'

    # Test for IntegrityError
    with pytest.raises(IntegrityError):
        wrong_task = Task(name=None)
        db.add(wrong_task)
        db.commit()
```

This unit test covers the basic functionality of the Item and Task models, including creation and error handling. The database used for testing is an in-memory SQLite database, which gets created for each test run and does not interfere with the actual database. Note that you have to replace "your_module" with the actual name of the module where your models are defined.