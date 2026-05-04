from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.dependencies.database import SessionLocal
from src.repositories.advertisement import AdRepository
from src.services.advertisement import AdService
from src.models import Advertisement as AdModel


def get_ad_repo(session: SessionLocal) -> AdRepository:
    return AdRepository(session=session)


def get_ad_service(
    session: SessionLocal,
    ad_repo: AdRepository = Depends(get_ad_repo),
) -> AdService:
    return AdService(
        session=session,
        ad_repo=ad_repo,
    )

AdServ = Annotated[AdService, Depends(get_ad_service)]

async def get_ad_from_query_param(
    advertisement_id: int,
    ad_repo: AdRepository = Depends(get_ad_repo),
) -> AdModel:
    ad = await ad_repo.get_by_id(advertisement_id)
    if ad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {advertisement_id} not found",
        )
    return ad




