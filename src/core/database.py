from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(url=settings.db.url, echo=False)
    session_local = async_sessionmaker(bind=engine, expire_on_commit=False)
    redis_client = Redis.from_url(settings.redis.url)

    app.state.engine = engine
    app.state.session_local = session_local
    app.state.redis_client = redis_client

    yield

    await app.state.engine.dispose()
    await app.state.redis_client.close()


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_local: async_sessionmaker[AsyncSession] = request.app.state.session_local
    async with session_local() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis(request: Request) -> Redis:
    redis_client: Redis = request.app.state.redis_client
    return redis_client
