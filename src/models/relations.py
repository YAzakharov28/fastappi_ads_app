# Связь пользователя и роли (многие-ко-многим)
from sqlalchemy import Column, ForeignKey, Table

from .base import Base

user_role_relation = Table(
    "user_role_relation",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True,
    ),  # Используем primary_key для составного ключа
    Column(
        "role_id",
        ForeignKey("roles.id"),
        primary_key=True,
    ),
)

# Связь роли и права (многие-ко-многим)
role_right_relation = Table(
    "role_right_relation",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("roles.id"),
        primary_key=True,
    ),
    Column(
        "right_id",
        ForeignKey("rights.id"),
        primary_key=True,
    ),
)
