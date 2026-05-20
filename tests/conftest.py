from uuid import UUID
import pytest_asyncio
from store.db.mongo import db_client
import pytest
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data
from tests.schemas.factories import products_data


@pytest.fixture(scope="session")
def mongo_client():
    return db_client.get()


@pytest_asyncio.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
def product_id() -> UUID:
    return UUID("3f1c9a5e-8b42-4d7f-9c6a-2e5b1a0f7d3c")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_update(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**data) for data in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product) for product in products_in]
