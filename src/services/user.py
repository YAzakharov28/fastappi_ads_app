from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import security
from src.models import User as UserModel
from src.repositories.user import UserRepository
from src.schemas.user import UserRegistrationRequest, UserUpdateRequest
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

    async def update_user(
        self,
        current_user: UserModel,
        user_for_update: UserModel,
        user_data: UserUpdateRequest,
    ) -> None:
        if user_data.role == "admin":
            # Проверяем, что мы не пытаемся себя повысить до админа
            if user_for_update.id == current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot self‑assign admin role",
                )
            # Проверяем, что запрос сделан админом
            if not await self.role_serv.is_admin(current_user):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admin can assign admin role",
                )

        can_update = await self.role_serv.check_object_access(
            user=current_user,
            orm_object=UserModel,
            need_write=True,
        )
        if not can_update:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        password = user_data.password
        if password is not None:
            user_for_update.hashed_password = security.hash_password(password)

        if user_data.username:
            user_for_update.username = user_data.username

        if user_data.role:
            role = await self.role_serv.get_role_by_name(user_data.role)
            user_for_update.roles = [role]

        await self.session.commit()
        await self.session.refresh(user_for_update)

    async def delete_user(self, user: UserModel) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def get_users_list(self, current_user: UserModel):
        has_access = await self.role_serv.check_object_access(
            user=current_user,
            orm_object=UserModel,
            need_read=True,
        )
        if not has_access:
            raise HTTPException(status_code=403, detail="Forbidden")

        return await self.user_repo.get_list()
