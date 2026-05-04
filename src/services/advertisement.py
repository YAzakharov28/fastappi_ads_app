from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.advertisement import AdRepository
from src.schemas.advertisement import AdCreateRequest, AdFilters, AdUpdateRequest
from src.models import Advertisement as AdModel


class AdService:
    def __init__(self, session: AsyncSession, ad_repo: AdRepository):
        self.session = session
        self.ad_repo = ad_repo

    async def create_advertisement(self, user_id: int, ad_data: AdCreateRequest) -> AdModel:
        advertisement = await self.ad_repo.create(user_id, ad_data)
        await self.session.commit()
        return advertisement

    async def update_advertisement(
            self,
            advertisement: AdModel,
            ad_data: AdUpdateRequest,
    ) -> None:
        update_data = ad_data.model_dump(exclude_unset=True, exclude_none=True)
        for attr, value in update_data.items():
            setattr(advertisement, attr, value)
        await self.session.commit()
        await self.session.refresh(advertisement)

    async def delete_advertisement(
        self,
        advertisement: AdModel,
    ) -> None:
        await self.session.delete(advertisement)
        await self.session.commit()

    async def get_advertisement_by_filters(
            self, filters_data: AdFilters
    ) -> dict[str, Any]:
        # Из-за того, что передаю в обработчике Query-параметры через Depends
        # Pydantic возвращает пользователю 500 ошибку
        # Поэтому валидирую это самостоятельно
        if filters_data.min_price is not None and filters_data.max_price is not None:
            if filters_data.min_price > filters_data.max_price:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="max_price must be greater than min_price",
                )

        result = await self.ad_repo.get_by_filters(filters_data)
        return result