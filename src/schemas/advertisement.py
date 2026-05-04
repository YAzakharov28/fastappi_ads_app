import enum
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator
from typing_extensions import Self


class AdCreateRequest(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=50,
        description="Заголовок объявления",
    )
    description: str = Field(
        description="Текст объявления",
    )
    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Цена объявления",
    )


class AdUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Заголовок объявления",
    )
    description: str | None = Field(
        default=None,
        description="Текст объявления",
    )
    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Цена объявления",
    )


    @model_validator(mode="after")
    def fields_validator(self) -> Self:
        if all(field is None for field in self.__dict__.values()):
            raise ValueError("No data to update")
        return self


class SortBy(enum.StrEnum):
    TITLE = "title"
    PRICE = "price"
    CREATED_AT = "created_at"
    USER_ID = "user_id"


class SortOrder(enum.StrEnum):
    ASC = "asc"
    DESC = "desc"


class AdFilters(BaseModel):
    page: int = Field(
        1,
        ge=1,
        description="Номер страницы",
    )
    page_size: int = Field(
        10,
        ge=1,
        le=100,
        description="Количество элементов на странице",
    )
    search: str | None = Field(
        None,
        min_length=1,
        description="Поиск по заголовку или описанию объявления",
    )
    min_price: Decimal | None = Field(
        None,
        ge=0,
        description="Минимальная цена объявления",
    )
    max_price: Decimal | None = Field(
        None,
        ge=0,
        description="Максимальная цена объявления",
    )
    user_id: int | None = Field(
        None,
        description="ID пользователя",
    )
    sort_by: SortBy = Field(
        SortBy.CREATED_AT,
        description="Поле для сортировки",
    )
    sort_order: SortOrder = Field(
        SortOrder.DESC,
        description="Направление сортировки",
    )


class AdResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    title: str
    description: str
    price: Decimal
    user_id: int
    created_at: datetime


class AdListResponse(BaseModel):
    items: list[AdResponse]
    total: int
    page: int
    page_size: int