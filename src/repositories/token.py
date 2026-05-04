from datetime import timedelta

from redis.asyncio import Redis

from src.core.config import settings


class TokenRedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    @staticmethod
    def _get_token_key(token_hash: str) -> str:
        return f"token:{token_hash}"

    async def add_token(self, token_hash: str, user_id: int, ttl: int) -> None:
        await self.redis_client.setex(
            name=self._get_token_key(token_hash),
            time=ttl,
            value=str(user_id),
        )

    async def get_user_id_by_token(self, token_hash: str) -> int | None:
        user_id = await self.redis_client.get(self._get_token_key(token_hash))
        return int(user_id) if user_id else None