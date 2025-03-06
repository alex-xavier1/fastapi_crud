To create a comprehensive unit test for the given module, we will use `pytest` and `SQLAlchemy`'s in-memory SQLite database for testing. We'll test the `Item` model's basic functionality, including its initialization and attribute constraints. We'll also address the issues in the `Task` model since it seems to have some typos or errors in the definition.

Here is a comprehensive unit test for the provided module:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from your_module import Base, Item, Task  # Replace 'your_module' with the actual module name

# Create an in-memory SQLite database and bind a session
@pytest.fixture(scope='function')
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_item_creation(session):
    # Test normal item creation
    item = Item(name="Test Item", description="A test item", price=100, quantity=10)
    session.add(item)
    session.commit()
    
    # Query the item back
    stored_item = session.query(Item).filter_by(name="Test Item").first()
    assert stored_item is not None
    assert stored_item.name == "Test Item"
    assert stored_item.description == "A test item"
    assert stored_item.price == 100
    assert stored_item.quantity == 10

def test_item_price_boundary(session):
    # Test edge case for price set to zero
    item = Item(name="Free Item", description="A free item", price=0, quantity=5)
    session.add(item)
    session.commit()
    
    stored_item = session.query(Item).filter_by(name="Free Item").first()
    assert stored_item.price == 0

    # Test negative price (should fail)
    with pytest.raises(IntegrityError):
        item = Item(name="Negative Price Item", description="Invalid item", price=-10, quantity=5)
        session.add(item)
        session.commit()

def test_item_quantity_boundary(session):
    # Test edge case for quantity as zero
    item = Item(name="Out of Stock Item", description="No stock", price=50, quantity=0)
    session.add(item)
    session.commit()
    
    stored_item = session.query(Item).filter_by(name="Out of Stock Item").first()
    assert stored_item.quantity == 0

    # Test negative quantity (should fail)
    with pytest.raises(IntegrityError):
        item = Item(name="Negative Quantity Item", description="Invalid item", price=50, quantity=-5)
        session.add(item)
        session.commit()

def test_task_creation(session):
    # Fixing the Task model definition
    class Task(Base):
        __tablename__ = "tasks"
        
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)

    Base.metadata.create_all(bind=session.get_bind())  # Recreate tables with Task

    # Test normal task creation
    task = Task(name="Test Task")
    session.add(task)
    session.commit()
    
    stored_task = session.query(Task).filter_by(name="Test Task").first()
    assert stored_task is not None
    assert stored_task.name == "Test Task"

def test_task_name_uniqueness(session):
    # Assuming Task names should be unique
    task1 = Task(name="Unique Task")
    session.add(task1)
    session.commit()
    
    # Attempt to add a task with the same name
    with pytest.raises(IntegrityError):
        task2 = Task(name="Unique Task")
        session.add(task2)
        session.commit()

```

### Key Points:

1. **Session Fixture