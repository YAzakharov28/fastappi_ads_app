from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.advertisement import AdCreateRequest, AdFilters, SortOrder
from src.models import Advertisement as AdModel, User as UserModel


class AdRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, advertisement_id: int) -> AdModel | None:
        ad = await self.session.get(AdModel, advertisement_id)
        return ad

    async def create(self, user_id: int, ad_data: AdCreateRequest) -> AdModel:
        advertisement = AdModel(**ad_data.model_dump())
        advertisement.user_id = user_id
        self.session.add(advertisement)
        return advertisement

    async def get_by_filters(self, filters_data: AdFilters):
        filters = []

        if filters_data.search is not None:
            search_value = filters_data.search.strip()
            if search_value:
                search_pattern = f"%{search_value.lower()}%"
                filters.append(
                    or_(
                        func.lower(AdModel.title).like(search_pattern),
                        func.lower(AdModel.description).like(search_pattern),
                    )
                )
        if filters_data.min_price is not None:
            filters.append(AdModel.price >= filters_data.min_price)
        if filters_data.max_price is not None:
            filters.append(AdModel.price <= filters_data.max_price)
        if filters_data.user_id is not None:
            filters.append(AdModel.user_id == filters_data.user_id)
        if filters_data.author:
            filters.append(UserModel.username.ilike(f"%{filters_data.author}%"))

        total_stmt = select(func.count()).select_from(AdModel).where(*filters)
        total = await self.session.scalar(total_stmt) or 0

        advertisements_stmt = (
            select(AdModel)
            .where(*filters)
            .offset((filters_data.page - 1) * filters_data.page_size)
            .limit(filters_data.page_size)
        )

        sort_field = getattr(AdModel, filters_data.sort_by.value)
        if filters_data.sort_order == SortOrder.DESC:
            stmt = advertisements_stmt.order_by(sort_field.desc())
        else:
            stmt = advertisements_stmt.order_by(sort_field.asc())

        items = (await self.session.scalars(stmt)).all()

        return {
            "items": items,
            "total": total,
            "page": filters_data.page,
            "page_size": filters_data.page_size,
        }