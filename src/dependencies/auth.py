from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.core import security
from src.dependencies.advertisement import get_ad_from_query_param
from src.dependencies.database import RedisClient, SessionLocal
from src.dependencies.user import get_user_from_query_param, get_user_repo
from src.models import Advertisement as AdModel, User as UserModel
from src.repositories.token import TokenRedisRepository
from src.repositories.user import UserRepository
from src.services.auth import AuthService
from src.services.role import RoleService


def get_token_repo(redis_client: RedisClient) -> TokenRedisRepository:
    return TokenRedisRepository(redis_client)


def get_auth_serv(
    session: SessionLocal,
    user_repo: UserRepository = Depends(get_user_repo),
    token_repo: TokenRedisRepository = Depends(get_token_repo),
) -> AuthService:
    return AuthService(
        session=session,
        user_repo=user_repo,
        token_repo=token_repo,
    )


def get_role_service(session: SessionLocal) -> RoleService:
    return RoleService(session)


async def get_current_user_id(
    user_token: str = Security(APIKeyHeader(name="x-token", auto_error=True)),
    token_repo: TokenRedisRepository = Depends(get_token_repo),
) -> int:
    token_hash = security.hash_token(user_token)
    user_id = await token_repo.get_user_id_by_token(token_hash)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user_id


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserModel:
    user_db = await user_repo.get_by_id(user_id)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user_db


async def get_user_write_access(
    user_for_write: UserModel = Depends(get_user_from_query_param),
    current_user: UserModel = Depends(get_current_user),
    role_serv: RoleService = Depends(get_role_service),
) -> UserModel:
    access = await role_serv.check_object_access(
        user=current_user,
        orm_object=user_for_write,
        need_write=True,
    )
    if not access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return user_for_write


async def get_ad_write_access(
    ad_for_write: AdModel = Depends(get_ad_from_query_param),
    current_user: UserModel = Depends(get_current_user),
    role_serv: RoleService = Depends(get_role_service),
) -> AdModel:
    access = await role_serv.check_object_access(
        user=current_user,
        orm_object=ad_for_write,
        need_write=True,
    )
    if not access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return ad_for_write
