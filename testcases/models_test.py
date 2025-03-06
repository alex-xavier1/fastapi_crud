# Here is an example of how you might write unit tests for the `Item` and `Task` models using pytest and SQLAlchemy's sessionmaker:


```python
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from my_module import Item, Task  # Assuming the above code is in my_module.py

# Create a mock engine and sessionmaker for SQLAlchemy
engine = Mock(spec=create_engine)
Session = Mock(spec=sessionmaker(bind=engine))

@pytest.fixture(scope='function')
def db():
    return Session()

def test_item_model(db):
    # Create a mock item
    mock_item = Item(id=1, name='Mock item', description='Mock description', price=100, quantity=10)
    db.add(mock_item)
    db.commit()

    # Test if the item is stored correctly
    item_in_db = db.query(Item).filter(Item.id == 1).first()
    assert item_in_db.id == mock_item.id
    assert item_in_db.name == mock_item.name
    assert item_in_db.description == mock_item.description
    assert item_in_db.price == mock_item.price
    assert item_in_db.quantity == mock_item.quantity

def test_task_model(db):
    # Create a mock task
    mock_task = Task(id=1, name='Mock task')
    db.add(mock_task)
    db.commit()

    # Test if the task is stored correctly
    task_in_db = db.query(Task).filter(Task.id == 1).first()
    assert task_in_db.id == mock_task.id
    assert task_in_db.name == mock_task.name

def test_item_model_edge_cases(db):
    # Test edge cases for Item model
    # An item with no name
    with pytest.raises(ValueError):
        mock_item = Item(id=1, name=None, description='Mock description', price=100, quantity=10)

    # An item with no price
    with pytest.raises(ValueError):
        mock_item = Item(id=1, name='Mock item', description='Mock description', price=None, quantity=10)

def test_task_model_edge_cases(db):
    # Test edge cases for Task model
    # A task with no name
    with pytest.raises(ValueError):
        mock_task = Task(id=1, name=None)
```

Note: In this script, we use `unittest.mock.Mock` to mock the SQLAlchemy engine and sessionmaker, which are external