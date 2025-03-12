# Unit test to verify the initialization and configuration of the FastAPI application

from unittest import IsolateAsyncioTestCase
from unittest.mock import patch, AsyncMock
from main import app
from fastapi.testclient import TestClient

class TestAppInitialization(IsolateAsyncioTestCase):
    
    @patch('main.Base.metadata.create_all', new_callable=AsyncMock)
    @patch('main.router')
    def test_app_initialization(self, mock_router, mock_create_all):
        with TestClient(app) as client:
            self.assertEqual(app.router, mock_router)
            mock_create_all.assert_called_once_with(bind=app.state.engine)