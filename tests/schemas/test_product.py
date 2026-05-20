from pydantic import ValidationError
import pytest
from store.schemas.product import ProductIn
from tests.schemas.factories import product_data


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 17 Pro Max"


def test_schemas_return_raise():
    data = {
        "name": "Iphone 17 Pro Max",
        "quantity": 10,
        "price": 999.99,
    }

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 17 Pro Max", "quantity": 10, "price": 999.99},
        "url": "https://errors.pydantic.dev/2.13/v/missing",
    }
