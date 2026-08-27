from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from app.config.settings import settings

redis_pool: aioredis.ConnectionPool = aioredis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=10,
)



async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    client = aioredis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()
