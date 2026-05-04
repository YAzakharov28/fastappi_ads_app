from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Role as RoleModel, User as UserModel, Right as RightModel, role_right_relation, \
    user_role_relation


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_object_access(
            self,
            user: UserModel,
            orm_object,  # Это может быть как класс модели (для создания), так и экземпляр (для чтения/изменения)
            need_read: bool = False,
            need_write: bool = False,
    ) -> bool:
        """
        Проверяет, есть ли у пользователя права на объект.
        """
        # 1. Определяем имя класса модели, к которой мы обращаемся
        model_class = orm_object if isinstance(orm_object, type) else orm_object.__class__
        model_name = model_class.__name__

        # 2. Формируем базовые условия для WHERE
        where_args = [
            UserModel.id == user.id,
            RightModel.model == model_name
        ]
        if need_read:
            where_args.append(RightModel.read == True)
        if need_write:
            where_args.append(RightModel.write == True)

        # 3. Особая логика для проверки "только свое" или "чужое".
            # Проверка на "свой" объект
            if not isinstance(orm_object, type):
                # Для модели User проверяем id
                if model_name == "User":
                    is_own = orm_object.id == user.id
                # Для других моделей проверяем user_id
                elif hasattr(orm_object, 'user_id'):
                    is_own = orm_object.user_id == user.id
                else:
                    is_own = True  # Если не определить принадлежность, считаем своим

                # Если объект не принадлежит текущему пользователю
                if not is_own:
                    where_args.append(RightModel.only_own == False)

        # 4. Формируем запрос на подсчет
        query = (
            select(func.count())
            .select_from(UserModel)
            .join(user_role_relation, UserModel.id == user_role_relation.c.user_id)
            .join(RoleModel, user_role_relation.c.role_id == RoleModel.id)
            .join(role_right_relation, RoleModel.id == role_right_relation.c.role_id)
            .join(RightModel, role_right_relation.c.right_id == RightModel.id)
            .where(*where_args)
        )

        # 5. Выполняем запрос
        count = await self.session.scalar(query)

        # 6. Если нашли хотя бы одно право - доступ разрешен
        return count > 0

    async def get_role_by_name(self, role_name: Literal["user", "admin"]) -> RoleModel:
        stmt = select(RoleModel).where(RoleModel.name == role_name)
        role_db = await self.session.scalar(stmt)
        return role_db

