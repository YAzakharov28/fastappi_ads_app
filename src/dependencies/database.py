from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session, get_redis

SessionLocal = Annotated[AsyncSession, Depends(get_async_session)]
RedisClient = Annotated[Redis, Depends(get_redis)]