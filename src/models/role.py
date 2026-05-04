from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import CreatedAtMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from .right import Right

class Role(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    rights: Mapped[list["Right"]] = relationship(
        secondary="role_right_relation",
        lazy="selectin",
    )
