import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings
from src.models import Right, Role


async def create_initial_roles(session: AsyncSession):
    """Создает базовые роли и права"""

    # --- Права ---
    # Право на изменение своих пользовательских данных
    right_read_wright_own_user = Right(
        read=True, write=True, only_own=True, model="User"
    )
    # Право на любые действия с пользователями (админское)
    right_full_user = Right(read=True, write=True, only_own=False, model="User")
    # Право на создание и изменение своих объявлений
    right_read_wright_own_ad = Right(
        read=True, write=True, only_own=True, model="Advertisement"
    )
    # Право на любые действия с объявлениями (админское)
    right_full_ad = Right(read=True, write=True, only_own=False, model="Advertisement")

    session.add_all(
        [
            right_read_wright_own_user,
            right_full_user,
            right_read_wright_own_ad,
            right_full_ad,
        ]
    )
    await session.flush()

    # --- Роли ---
    role_user = Role(name="user")
    role_user.rights = [right_read_wright_own_user, right_read_wright_own_ad]

    role_admin = Role(name="admin")
    role_admin.rights = [right_full_user, right_full_ad]

    session.add_all([role_user, role_admin])
    await session.commit()


async def main():
    engine = create_async_engine(url=settings.db.url, echo=False)
    session_local = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session_local() as session:
        try:
            await create_initial_roles(session)
            print("Initial roles are created!")
        except SQLAlchemyError as err:
            await session.rollback()
            print(f"Error: {str(err)}")


if __name__ == "__main__":
    asyncio.run(main())
