from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.models import User as UserModel
from src.repositories.user import UserRepository
from src.services.role import RoleService
from src.services.user import UserService
from .database import SessionLocal


def get_user_service(session: SessionLocal) -> UserService:
    return UserService(
        session=session,
        user_repo=UserRepository(session),
        role_serv=RoleService(session),
    )


def get_user_repo(session: SessionLocal) -> UserRepository:
    return UserRepository(session)


async def get_user_from_query_param(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserModel:
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


UserServ = Annotated[UserService, Depends(get_user_service)]
