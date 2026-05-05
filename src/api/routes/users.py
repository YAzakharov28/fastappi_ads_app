from fastapi import APIRouter, Depends, status

from src.dependencies.auth import (
    get_current_user,
    get_user_from_query_param,
    get_user_write_access,
)
from src.dependencies.user import UserServ
from src.models import User as UserModel
from src.schemas.user import UserRegistrationRequest, UserResponse, UserUpdateRequest

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/", response_model=list[UserModel])
async def get_users_list(
    user_serv: UserServ,
    current_user: UserModel = Depends(get_current_user),
):
    users_list = await user_serv.get_users_list(current_user)
    return users_list


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    user_data: UserRegistrationRequest,
    user_serv: UserServ,
):
    new_user = await user_serv.user_registration(user_data)
    return new_user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_serv: UserServ,
    user_data: UserUpdateRequest,
    user_for_update: UserModel = Depends(get_user_from_query_param),
    current_user: UserModel = Depends(get_current_user),
):
    await user_serv.update_user(current_user, user_for_update, user_data)
    return user_for_update


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_serv: UserServ,
    user: UserModel = Depends(get_user_write_access),
):
    await user_serv.delete_user(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user_by_id(
    user: UserModel = Depends(get_user_from_query_param),
):
    return user
