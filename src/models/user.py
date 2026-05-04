from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntPrimaryKeyMixin, TimeStampMixin

if TYPE_CHECKING:
    from .advertisement import Advertisement
    from .role import Role


class User(IntPrimaryKeyMixin, TimeStampMixin, Base):
    username: Mapped[str] = mapped_column(String(50), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    advertisements: Mapped[list["Advertisement"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    roles: Mapped[list["Role"]] = relationship(
        secondary="user_role_relation",
        lazy="selectin",
    )

    __table_args__ = (UniqueConstraint("username"),)