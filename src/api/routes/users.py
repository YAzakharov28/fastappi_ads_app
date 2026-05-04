from fastapi import APIRouter, Depends, status

from src.dependencies.auth import get_user_from_query_param, get_user_write_access
from src.dependencies.user import UserServ
from src.models import User as UserModel
from src.schemas.user import UserRegistrationRequest, UserResponse, UserUpdateRequest

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


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
    user: UserModel = Depends(get_user_write_access),
):
    await user_serv.update_user(user, user_data)
    return user


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
