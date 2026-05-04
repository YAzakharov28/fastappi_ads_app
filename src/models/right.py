from typing import Literal

from sqlalchemy import String, false, true
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import CreatedAtMixin, UUIDPrimaryKeyMixin

ModelName = Literal["User", "Advertisement", "Role", "Right"]


class Right(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    # Может ли писать (создавать/изменять/удалять)
    write: Mapped[bool] = mapped_column(server_default=false())
    # Может ли читать
    read: Mapped[bool] = mapped_column(server_default=false())
    # Только свои записи или любые
    only_own: Mapped[bool] = mapped_column(server_default=true())
    # Имя модели. Будет храниться строго одно из значений ModelName
    model: Mapped[ModelName] = mapped_column(String(50))
