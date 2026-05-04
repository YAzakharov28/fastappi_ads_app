from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntPrimaryKeyMixin, TimeStampMixin

if TYPE_CHECKING:
    from .user import User


class Advertisement(IntPrimaryKeyMixin, TimeStampMixin, Base):

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(
        back_populates="advertisements",
        lazy="selectin",
    )
