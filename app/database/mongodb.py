from motor.motor_asyncio import AsyncIOMotorClient
from ..config import get_settings

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        await self._create_indexes()

    async def _create_indexes(self):
        # Create indexes for better query performance
        await self.db.users.create_index("email", unique=True)
        await self.db.users.create_index("username")
        await self.db.teams.create_index("team_name")
        await self.db.teams.create_index([("conference", 1), ("position", 1)])
        await self.db.teams.create_index("favorite_teams")

    async def close(self):
        if self.client:
            self.client.close()

    async def get_db(self):
        return self.db

mongodb = MongoDB() 