from decimal import Decimal
from uuid import UUID
import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_sucess(product_in):
    result = await product_usecase.create(body=product_in)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 17 Pro Max"


async def test_usecases_get_should_return_sucess(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 17 Pro Max"


async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as exc_info:
        await product_usecase.get(id=UUID("3f1c9a5e-8b42-4d7f-9c6a-2e5b1a0f7d3c"))

    assert (
        exc_info.value.message
        == "Product not found with id: 3f1c9a5e-8b42-4d7f-9c6a-2e5b1a0f7d3c"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_sucess(products_inserted):
    result = await product_usecase.query()
    assert isinstance(result, list)
    assert len(result) > 1


async def test_usecases_update_should_return_sucess(product_update, product_inserted):
    initial_product = ProductIn(
        id=product_inserted.id,
        name="Iphone 17 Pro Max",
        quantity=10,
        price=Decimal("5000.00"),
        status=True,
    )
    await product_usecase.create(body=initial_product)
    product_update.price = Decimal("7500.00")
    result = await product_usecase.update(id=product_inserted.id, body=product_update)
    assert isinstance(result, ProductUpdateOut)
    assert result.price == Decimal("7500.00")


async def test_usecases_delete_should_return_success(product_inserted):
    initial_product = ProductIn(
        id=product_inserted.id,
        name="Iphone 17 Pro Max",
        quantity=10,
        price=Decimal("5000.00"),
        status=True,
    )

    await product_usecase.create(body=initial_product)
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True


async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as exc_info:
        await product_usecase.get(id=UUID("3f1c9a5e-8b42-4d7f-9c6a-2e5b1a0f7d3c"))

    assert (
        exc_info.value.message
        == "Product not found with id: 3f1c9a5e-8b42-4d7f-9c6a-2e5b1a0f7d3c"
    )
