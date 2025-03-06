# Sure, here's a simple unit test for the Item models.


```python
import pytest
from pydantic import ValidationError
from main import ItemCreate, ItemResponse

def test_item_create():
    # Test successful creation
    item = ItemCreate(name="test", description="test item", price=100, quantity=10)
    assert item.name == "test"
    assert item.description == "test item"
    assert item.price == 100
    assert item.quantity == 10

    # Test missing fields
    with pytest.raises(ValidationError):
        ItemCreate()

    # Test price and quantity as negative values
    with pytest.raises(ValidationError):
        ItemCreate(name="test", description="test item", price=-100, quantity=10)

    with pytest.raises(ValidationError):
        ItemCreate(name="test", description="test item", price=100, quantity=-10)

    # Test price and quantity as non-integer values
    with pytest.raises(ValidationError):
        ItemCreate(name="test", description="test item", price=100.5, quantity=10)

    with pytest.raises(ValidationError):
        ItemCreate(name="test", description="test item", price=100, quantity=10.5)


def test_item_response():
    # Test successful creation
    item = ItemResponse(id=1, name="test", description="test item", price=100, quantity=10)
    assert item.id == 1
    assert item.name == "test"
    assert item.description == "test item"
    assert item.price == 100
    assert item.quantity == 10

    # Test missing fields
    with pytest.raises(ValidationError):
        ItemResponse()

    # Test item id as negative value
    with pytest.raises(ValidationError):
        ItemResponse(id=-1, name="test", description="test item", price=100, quantity=10)

    # Test item id as non-integer value
    with pytest.raises(ValidationError):
        ItemResponse(id=1.5, name="test", description="test item", price=100, quantity=10)
```

This test covers:
- Valid item creation
- Missing required fields
- Invalid types for fields
- Negative values for fields that should only have positive values

It does not include any dependencies, as the models do not interact with any external services.