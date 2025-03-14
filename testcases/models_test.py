# Unit tests for the Item and Task models, ensuring correct schema definition and handling of edge cases.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_module import Base, Item, Task

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_item_model():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    item = Item(name="Test Item", description="Test Description", price=100, quantity=5)
    db.add(item)
    db.commit()
    db.refresh(item)
    assert item.id is not None
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.price == 100
    assert item.quantity == 5

def test_task_model():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    task = Task(name="Test Task")
    db.add(task)
    db.commit()
    db.refresh(task)
    assert task.id is not None
    assert task.name == "Test Task"

def test_item_model_edge_cases():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    item = Item(name="", description="Test Description", price=-100, quantity=-5)
    with pytest.raises(Exception):
        db.add(item)
        db.commit()

def test_task_model_edge_cases():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    task = Task(name="")
    with pytest.raises(Exception):
        db.add(task)
        db.commit()