from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User as UserModel
from src.repositories.user import UserRepository
from src.schemas.user import UserRegistrationRequest, UserUpdateRequest
from src.core import security
from src.services.role import RoleService


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
        role_serv: RoleService,
    ):
        self.session = session
        self.user_repo = user_repo
        self.role_serv = role_serv

    async def user_registration(
        self,
        user_data: UserRegistrationRequest,
        user_role: Literal["user", "admin"] = "user",
    ) -> UserModel | None:
        role_db = await self.role_serv.get_role_by_name(user_role)
        new_user = await self.user_repo.create(
            username=user_data.username,
            hashed_password=security.hash_password(user_data.password),
            role=role_db,
        )
        try:
            await self.session.commit()
            return new_user
        except IntegrityError as err:
            msg = str(err.orig).lower()
            if "username" in msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists",
                )

    async def update_user(self, user: UserModel, user_data: UserUpdateRequest) -> None:
        password = user_data.password
        if password is not None:
            user_data.password = security.hash_password(password)
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)

    async def delete_user(self, user: UserModel) -> None:
        await self.session.delete(user)
        await self.session.commit()
