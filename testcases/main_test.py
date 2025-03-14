# Unit test for the FastAPI application initialization and route inclusion

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, Base, engine, router

@patch('database.engine')
@patch('models.Base')
def test_app_initialization(mock_base, mock_engine):
    mock_base.metadata.create_all = MagicMock()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 404
    mock_base.metadata.create_all.assert_called_once_with(bind=mock_engine)
    assert app.router.routes == router.routes