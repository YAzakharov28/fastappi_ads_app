from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Role as RoleModel, User as UserModel
from src.schemas.user import UserUpdateRequest


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.username == username)
        user_db = await self.session.scalar(stmt)
        return user_db

    async def get_by_id(self, user_id: int) -> UserModel | None:
        user_db = await self.session.get(UserModel, user_id)
        return user_db

    async def create(
        self,
        username: str,
        hashed_password: str,
        role: RoleModel,
    ) -> UserModel:
        new_user = UserModel(
            username=username,
            hashed_password=hashed_password,
        )
        new_user.roles = [role]
        self.session.add(new_user)
        return new_user

