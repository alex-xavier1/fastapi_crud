# ```python

# Unit tests for ItemBase, ItemCreate, and ItemResponse classes

from pydantic import ValidationError
from models import ItemBase, ItemCreate, ItemResponse
import pytest

# Test ItemBase model
def test_item_base_model():
    item = ItemBase(name="Test Item", description="This is a test item", price=20, quantity=5)
    
    assert item.name == "Test Item"
    assert item.description == "This is a test item"
    assert item.price == 20
    assert item.quantity == 5

# Test ItemBase model with wrong data types
def test_item_base_model_wrong_data_types():
    with pytest.raises(ValidationError):
        item = ItemBase(name=1234, description="This is a test item", price="20", quantity="5")

# Test ItemCreate model
def test_item_create_model():
    item = ItemCreate(name="Test Item", description="This is a test item", price=20, quantity=5)
    
    assert item.name == "Test Item"
    assert item.description == "This is a test item"
    assert item.price == 20
    assert item.quantity == 5

# Test ItemCreate model with wrong data types
def test_item_create_model_wrong_data_types():
    with pytest.raises(ValidationError):
        item = ItemCreate(name=1234, description="This is a test item", price="20", quantity="5")

# Test ItemResponse model
def test_item_response_model():
    item = ItemResponse(id=1, name="Test Item", description="This is a test item", price=20, quantity=5)
    
    assert item.id == 1
    assert item.name == "Test Item"
    assert item.description == "This is a test item"
    assert item.price == 20
    assert item.quantity == 5

# Test ItemResponse model with wrong data types
def test_item_response_model_wrong_data_types():
    with pytest.raises(ValidationError):
        item = ItemResponse(id="1", name="Test Item", description="This is a test item", price=20, quantity=5)
```

This test file includes tests for each of the models. The tests check that each model correctly instantiates with valid data and raises a ValidationError when instantiated with invalid data. The test file does not mock any external dependencies such as APIs, databases, or authentication services because these are not used in the models.