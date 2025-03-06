# ```python

from fastapi.testclient import TestClient
from unittest import TestCase
from unittest.mock import patch
from main import app, ItemBase, ItemCreate, ItemResponse
import json

class TestItemModels(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.item_data = {
            'name': 'Test Item',
            'description': 'This is a test item',
            'price': 100,
            'quantity': 10
        }

    def test_item_base_model(self):
        item_base = ItemBase(**self.item_data)
        self.assertEqual(item_base.name, 'Test Item')
        self.assertEqual(item_base.description, 'This is a test item')
        self.assertEqual(item_base.price, 100)
        self.assertEqual(item_base.quantity, 10)

    def test_item_create_model(self):
        item_create = ItemCreate(**self.item_data)
        self.assertEqual(item_create.name, 'Test Item')
        self.assertEqual(item_create.description, 'This is a test item')
        self.assertEqual(item_create.price, 100)
        self.assertEqual(item_create.quantity, 10)

    @patch('main.get_db')
    def test_item_response_model(self, mock_get_db):
        item_response_data = self.item_data.copy()
        item_response_data.update({'id': 1})
        item_response = ItemResponse(**item_response_data)
        self.assertEqual(item_response.id, 1)
        self.assertEqual(item_response.name, 'Test Item')
        self.assertEqual(item_response.description, 'This is a test item')
        self.assertEqual(item_response.price, 100)
        self.assertEqual(item_response.quantity, 10)

    @patch('main.get_db')
    def test_create_item(self, mock_get_db):
        response = self.client.post('/items/', data=json.dumps(self.item_data))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), self.item_data)

    @patch('main.get_db')
    def test_get_item(self, mock_get_db):
        mock_get_db.return_value.get.return_value = ItemResponse(**self.item_data, id=1)
        response = self.client.get('/items/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.item_data)

    @patch('main.get_db')
    def test_get_item_not_found(self, mock_get_db):
        mock_get_db.return_value.get.return_value = None
        response = self.client.get