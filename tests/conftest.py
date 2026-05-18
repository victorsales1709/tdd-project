import asyncio
from uuid import UUID
import pytest_asyncio
from store.db.mongo import db_client
import pytest
from store.schemas.product import ProductIn
from tests.factories import product_data


@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mongo_client():
    return db_client.get()


@pytest_asyncio.fixture(autouse=True)
async def clear_collections(mongo_client, event_loop):
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
