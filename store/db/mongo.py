from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings


class MongoClient:
    def get(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.DATABASE_URL)


db_client = MongoClient()
