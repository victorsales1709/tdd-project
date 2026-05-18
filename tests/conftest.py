import asyncio
import pytest_asyncio
from store.db.mongo import db_client
import pytest


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
