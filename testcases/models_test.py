# ```python

# Unit tests for the Item and Task models in FastAPI using SQLAlchemy ORM

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Item, Task

# Mocking a SQLAlchemy Session for testing
@pytest.fixture
def db_session() -> Session:
    engine = create_engine('sqlite:///:memory:', echo=True)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_create_item(db_session):
    item = Item(name='Test Item', description='Item for testing', price=100, quantity=10)
    db_session.add(item)
    db_session.commit()
    assert item in db_session

def test_item_not_found(db_session):
    item = db_session.query(Item).filter_by(name='Non-existent item').first()
    assert item is None

def test_create_task(db_session):
    task = Task(name='Test Task')
    db_session.add(task)
    db_session.commit()
    assert task in db_session

def test_task_not_found(db_session):
    task = db_session.query(Task).filter_by(name='Non-existent task').first()
    assert task is None

def test_update_item(db_session):
    item = Item(name='Test Item', description='Item for testing', price=100, quantity=10)
    db_session.add(item)
    db_session.commit()
    item.price = 200
    db_session.commit()
    assert item.price == 200

def test_update_task(db_session):
    task = Task(name='Test Task')
    db_session.add(task)
    db_session.commit()
    task.name = 'Updated Task'
    db_session.commit()
    assert task.name == 'Updated Task'

def test_delete_item(db_session):
    item = Item(name='Test Item', description='Item for testing', price=100, quantity=10)
    db_session.add(item)
    db_session.commit()
    db_session.delete(item)
    db_session.commit()
    assert item not in db_session

def test_delete_task(db_session):
    task = Task(name='Test Task')
    db_session.add(task)
    db_session.commit()
    db_session.delete(task)
    db_session.commit()
    assert task not in db_session
```
Please note that the models used here are from the given module. The test cases cover all CRUD operations for the models.