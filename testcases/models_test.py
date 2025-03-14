# Unit test to verify the database models Item and Task structure and integrity

from unittest import TestCase, mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_module import Base, Item, Task

class TestDatabaseModels(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_item_model(self):
        item = Item(name="Test Item", description="Test Description", price=100, quantity=50)
        self.session.add(item)
        self.session.commit()
        retrieved_item = self.session.query(Item).filter(Item.name == "Test Item").first()
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.description, "Test Description")
        self.assertEqual(retrieved_item.price, 100)
        self.assertEqual(retrieved_item.quantity, 50)

    def test_task_model(self):
        task = Task(name="Test Task")
        self.session.add(task)
        self.session.commit()
        retrieved_task = self.session.query(Task).filter(Task.name == "Test Task").first()
        self.assertIsNotNone(retrieved_task)