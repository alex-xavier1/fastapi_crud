To create a comprehensive unit test for the given module, we should focus on testing the interactions with the database engine and session creation. Since the actual database should not be accessed during unit testing, we will mock external dependencies using the `unittest.mock` library. Below is the testing code using `pytest` and `unittest.mock`:

```python
import os
from unittest import mock
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# The module under test
import my_database_module  # replace with the actual module name

@pytest.fixture
def mock_env_vars(monkeypatch):
    # Mock the DATABASE_URL environment variable
    monkeypatch.setenv("DATABASE_URL", "postgresql://test_user:test_password@localhost/test_db")

@pytest.fixture
def mock_create_engine():
    with mock.patch('my_database_module.create_engine') as mock_engine:
        yield mock_engine

@pytest.fixture
def mock_sessionmaker():
    with mock.patch('my_database_module.sessionmaker') as mock_session:
        yield mock_session

def test_database_url_default(monkeypatch):
    # Remove the DATABASE_URL to test the default
    monkeypatch.delenv("DATABASE_URL", raising=False)
    from my_database_module import DATABASE_URL
    assert DATABASE_URL == "postgresql://user:password@localhost/fastapi_db"

def test_database_url_env_var(mock_env_vars):
    from my_database_module import DATABASE_URL
    assert DATABASE_URL == "postgresql://test_user:test_password@localhost/test_db"

def test_engine_creation(mock_env_vars, mock_create_engine):
    from my_database_module import engine
    mock_create_engine.assert_called_once_with("postgresql://test_user:test_password@localhost/test_db")
    assert engine is mock_create_engine.return_value

def test_session_local_creation(mock_sessionmaker):
    from my_database_module import SessionLocal
    mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=mock.ANY)
    assert SessionLocal is mock_sessionmaker.return_value

def test_base_declaration():
    from my_database_module import Base
    assert isinstance(Base, type(declarative_base()))
```

### Explanation:

1. **Fixtures**:
   - `mock_env_vars`: Sets up the environment variable `DATABASE_URL` using `monkeypatch` to simulate different configurations.
   - `mock_create_engine` and `mock_sessionmaker`: Use `unittest.mock.patch` to mock `create_engine` and `sessionmaker` to prevent actual database operations.

2. **Test Cases**:
   - `test_database_url_default`: Verifies that the default `DATABASE_URL` is used when the environment variable is not set.
   - `test_database_url_env_var`: Confirms that the environment variable `DATABASE_URL` is correctly read and used.
   - `test_engine_creation`: Ensures that `create_engine` is called with the correct database URL.
   - `test_session_local_creation`: Checks that `sessionmaker` is configured with the expected parameters.
   - `test_base_declaration`: Verifies that `Base` is correctly set up as a declarative base.

### Best Practices:
- **Isolation**: Each test case is isolated, ensuring no side effects between tests.
- **Mocking**: External database connections are mocked to ensure that tests are not dependent on the actual database.
- **Assertions**: Meaningful assertions ensure that the code behaves as expected under different scenarios.
- **Readability**: Tests are written clearly, making it easy for other developers to understand the purpose of each test.