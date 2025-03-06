# Here is an example of a unit test for the given module using pytest and pytest-mock:


```python
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# MODULE TO BE TESTED
from your_package import your_module

# SETUP FIXTURES

@pytest.fixture
def mock_os_environ_get(mocker):
    return mocker.patch('os.environ.get')

@pytest.fixture
def mock_create_engine(mocker):
    return mocker.patch('sqlalchemy.create_engine')

@pytest.fixture
def mock_sessionmaker(mocker):
    return mocker.patch('sqlalchemy.orm.sessionmaker')

@pytest.fixture
def mock_declarative_base(mocker):
    return mocker.patch('sqlalchemy.ext.declarative_base')


# UNIT TESTS

def test_database_url(mock_os_environ_get):
    mock_os_environ_get.return_value = 'test_url'
    reload(your_module)
    assert your_module.DATABASE_URL == 'test_url'
    mock_os_environ_get.assert_called_once_with("DATABASE_URL", "postgresql://user:password@localhost/fastapi_db")

def test_engine_creation(mock_os_environ_get, mock_create_engine):
    mock_os_environ_get.return_value = 'test_url'
    reload(your_module)
    mock_create_engine.assert_called_once_with('test_url')

def test_session_creation(mock_sessionmaker):
    mock_session = MagicMock()
    mock_sessionmaker.return_value = mock_session
    reload(your_module)
    assert your_module.SessionLocal == mock_session
    mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=your_module.engine)

def test_base_creation(mock_declarative_base):
    mock_base = MagicMock()
    mock_declarative_base.return_value = mock_base
    reload(your_module)
    assert your_module.Base == mock_base
    mock_declarative_base.assert_called_once()
```

This suite of unit tests ensures that all key functions within the module are tested, including environment variable retrieval, engine creation, session creation, and base creation. Each test case uses mock to replace the real dependencies with fake ones, allowing us to control their behavior for testing scenarios. This way we ensure that our tests are isolated and deterministic.

Remember to replace `your_package` and `your_module` with the actual package and module names.