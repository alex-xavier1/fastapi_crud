# Unit tests for models.py

Here is an example of a unit test for the above module using pytest and mock. We are testing the Item and Task models in isolation, hence we mock the SQLAlchemy session and other external dependencies. We also test some edge cases, errors and boundary values.

```python
# This unit test is for testing the Item and Task models in our application.

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from your_module import Item, Task

@patch('sqlalchemy.orm.Session')
def test_item_model(mocked_session):
    # Instantiate the Item model
    item = Item(id=1, name='Test Item', description='This is a test item', price=100, quantity=20)

    # Test normal case: save item
    mocked_session.add.assert_called_once()
    mocked_session.commit.assert_called_once()

    # Test edge case: save item with blank name
    item.name = ''
    with pytest.raises(ValueError):
        item.save()

    # Test error case: database error
    mocked_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        item.save()

    # Test boundary value: price is 0
    item.price = 0
    assert item.save() is True

@patch('sqlalchemy.orm.Session')
def test_task_model(mocked_session):
    # Instantiate the Task model
    task = Task(id=1, name='Test Task')

    # Test normal case: save task
    mocked_session.add.assert_called_once()
    mocked_session.commit.assert_called_once()

    # Test edge case: save task with blank name
    task.name = ''
    with pytest.raises(ValueError):
        task.save()

    # Test error case: database error
    mocked_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        task.save()

# Execute the test suite
if __name__ == "__main__":
    pytest.main()
```
Please note that this example assumes the Item and Task models have a save() method that adds the instance to the session and commits it. If this is not the case, you will need to adjust the test accordingly. Also, replace "your_module" with the actual name of the module where Item and Task are defined.

Also note, in the example above, the sqlalchemy.orm.Session is patched. However, in a real-world application, the session is usually part of a higher-level component (like a database service). In that case, you would want to patch that component instead.