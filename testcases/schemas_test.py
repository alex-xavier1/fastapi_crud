To create a comprehensive unit test for the provided module using FastAPI and Pydantic, we can utilize the `pytest` framework. Since the module mainly defines Pydantic models, we don't have any external dependencies or FastAPI routes to mock. Our focus will be on testing the model's validation logic.

Here is the unit test code:

```python
import pytest
from pydantic import ValidationError
from your_module_name import ItemBase, ItemCreate, ItemResponse


def test_item_base_valid_data():
    item = ItemBase(name="Test Item", description="A test item", price=100, quantity=10)
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 100
    assert item.quantity == 10


def test_item_base_missing_name():
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(description="A test item", price=100, quantity=10)
    assert "field required" in str(exc_info.value)


def test_item_base_negative_price():
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="Test Item", description="A test item", price=-100, quantity=10)
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)


def test_item_base_zero_quantity():
    item = ItemBase(name="Test Item", description="A test item", price=100, quantity=0)
    assert item.quantity == 0


def test_item_create_inherits_item_base():
    item = ItemCreate(name="Test Item", description="A test item", price=100, quantity=10)
    assert isinstance(item, ItemBase)


def test_item_response_valid_data():
    item = ItemResponse(id=1, name="Test Item", description="A test item", price=100, quantity=10)
    assert item.id == 1
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 100
    assert item.quantity == 10


def test_item_response_orm_mode():
    class MockORMItem:
        def __init__(self, id, name, description, price, quantity):
            self.id = id
            self.name = name
            self.description = description
            self.price = price
            self.quantity = quantity

    orm_item = MockORMItem(id=1, name="ORM Item", description="An ORM item", price=200, quantity=5)
    item_response = ItemResponse.from_orm(orm_item)
    assert item_response.id == orm_item.id
    assert item_response.name == orm_item.name
    assert item_response.description == orm_item.description
    assert item_response.price == orm_item.price
    assert item_response.quantity == orm_item.quantity


def test_item_response_missing_id():
    with pytest.raises(ValidationError) as exc_info:
        ItemResponse(name="Test Item", description="A test item", price=100, quantity=10)
    assert "field required" in str(exc_info.value)
```

### Explanation:
- **Test Setup:** We use `pytest` for testing because it provides a simple and effective way to write tests for Python applications.
- **Validation Tests:** We verify that the Pydantic models correctly enforce data validation constraints such as required fields and non-negative prices.
- **Inheritance Tests:** We check that `ItemCreate` inherits from `ItemBase` correctly.
- **ORM Mode Tests:** We mock an ORM-like object to ensure the `orm_mode` configuration works as expected in the `ItemResponse` model.
- **Boundary and Edge Cases:** We test boundary conditions such as zero quantity and negative price to see how the models handle these inputs.

These tests provide a robust way to ensure that the Pydantic models behave as expected under various conditions. Adjust the module import