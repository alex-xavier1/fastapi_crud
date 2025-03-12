# Unit test to verify the schema and attributes of Item and Task models

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

    def test_item_model(self):
        item = Item(name="Test Item", description="Test Description", price=100, quantity=50)
        self.session.add(item)
        self.session.commit()
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "Test Description")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.quantity, 50)

    def test_task_model(self):
        task = Task(name="Test Task")
        self.session.add(task)
        self.session.commit()
        self.assertEqual(task.name, "Test Task")