# Unit tests for models.py

```python
# Unit tests for Item and Task models to ensure correct initialization and attribute handling

from unittest import TestCase, mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_module import Base, Item, Task

class TestModels(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def test_item_initialization(self):
        item = Item(name="Test Item", description="Test Description", price=100, quantity=5)
        self.session.add(item)
        self.session.commit()
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "Test Description")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 5)

    def test_item_missing_name(self):
        with self.assertRaises(TypeError):
            item = Item(description="Test Description", price=100, quantity=5)

    def test_item_negative_price(self):
        with self.assertRaises(ValueError):
            item = Item(name="Test Item", description="Test Description", price=-100, quantity=5)

    def test_item_zero_quantity(self):
        item = Item(name="Test Item", description="Test Description", price=100, quantity=0)
        self.session.add(item)
        self.session.commit()
        self.assertEqual(item.quantity, 0)

    def test_task_initialization(self):
        with mock.patch('sqlalchemy.ext.declarative.declarative_base.classes.Task') as MockTask:
            MockTask.id = mock.MagicMock()
            MockTask.name = mock.MagicMock()
            task = Task()
            self.assertTrue(hasattr(task, 'id'))
            self.assertTrue(hasattr(task, 'name'))
```