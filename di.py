# di.py
import asyncio
import asyncpg
from settings import settings

class Container:
    _pool = None

    @classmethod
    async def init(cls):
        cls._pool = await asyncpg.create_pool(dsn=settings.DB_DSN)

    @classmethod
    def pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError("Container is not initialized")
        return cls._pool
