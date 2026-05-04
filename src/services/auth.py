from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import security
from src.core.config import settings
from src.repositories.token import TokenRedisRepository
from src.repositories.user import UserRepository
from src.schemas.auth import LoginRequest, LoginResponse


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
        token_repo: TokenRedisRepository,
    ):
        self.session = session
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def login(self, credentials: LoginRequest):
        user_db = await self.user_repo.get_by_username(credentials.username)
        if user_db is None or not security.verify_password(
            password=credentials.password,
            password_hash=user_db.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials",
            )

        raw_token, token_hash = security.generate_token()
        ttl = int(timedelta(hours=settings.token.expire_hours).total_seconds())
        await self.token_repo.add_token(token_hash, user_db.id, ttl)
        return LoginResponse(token=raw_token)
