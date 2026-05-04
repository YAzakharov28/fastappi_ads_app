from fastapi import APIRouter, Depends

from src.dependencies.auth import get_auth_serv
from src.schemas.auth import LoginRequest, LoginResponse
from src.services.auth import AuthService

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    credentials: LoginRequest,
    auth_serv: AuthService = Depends(get_auth_serv),
):
    token = await auth_serv.login(credentials)
    return token


