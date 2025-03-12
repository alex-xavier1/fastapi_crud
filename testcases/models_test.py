# Unit test to verify the schema definitions and basic operations of Item and Task models

from unittest import IsolateTestCase
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_module import Base, Item, Task

class TestModels(IsolateTestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_item_model(self):
        item = Item(name="Test Item", description="Test Description", price=100, quantity=5)
        self.session.add(item)
        self.session.commit()
        retrieved_item = self.session.query(Item).filter(Item.name == "Test Item").first()
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.name, "Test Item")
        self.assertEqual(retrieved_item.description, "Test Description")
        self.assertEqual(retrieved_item.price, 100)
        self.assertEqual(retrieved_item.quantity, 5)

    def test_task_model(self):
        with self.assertRaises(AttributeError):
            task = Task(name="Test Task")
            self.session.add(task)
            self.session.commit()