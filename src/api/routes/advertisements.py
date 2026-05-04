from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.dependencies.advertisement import AdServ, get_ad_from_query_param
from src.dependencies.auth import get_ad_write_access, get_current_user
from src.models import Advertisement as AdModel, User as UserModel
from src.schemas.advertisement import (
    AdCreateRequest,
    AdFilters,
    AdListResponse,
    AdResponse,
    AdUpdateRequest,
)

router = APIRouter(
    prefix="/advertisements",
    tags=["Advertisement"],
)


@router.get(
    "/{advertisement_id}",
    response_model=AdResponse,
)
async def get_advertisement(ad: AdModel = Depends(get_ad_from_query_param)):
    return ad


@router.get(
    "/",
    response_model=AdListResponse,
)
async def get_advertisement_by_filters(
    filters_data: Annotated[AdFilters, Depends()],
    ad_service: AdServ,
):
    result = await ad_service.get_advertisement_by_filters(filters_data)
    return result


@router.post(
    "/",
    response_model=AdResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_advertisement(
    ad_data: AdCreateRequest,
    ad_service: AdServ,
    current_user: UserModel = Depends(get_current_user),
):
    ad = await ad_service.create_advertisement(current_user.id, ad_data)
    return ad


@router.patch(
    "/{advertisement_id}",
    response_model=AdResponse,
)
async def update_advertisement(
    ad_data: AdUpdateRequest,
    ad_service: AdServ,
    advertisement: AdModel = Depends(get_ad_write_access),
):
    await ad_service.update_advertisement(advertisement, ad_data)
    return advertisement


@router.delete(
    "/{advertisement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_advertisement(
    ad_service: AdServ,
    advertisement: AdModel = Depends(get_ad_write_access),
):
    await ad_service.delete_advertisement(advertisement)
