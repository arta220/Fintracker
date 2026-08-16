
from fastapi import APIRouter, Depends, Response
from starlette import status
from app.DTO.user import *
from app.api.v1.dependency.dependency import get_current_user_from_refresh
from app.api.v1.dependency.dependency import get_auth_service
from app.service import AuthService, jwt_service
from app.repository.db_models import *

router = APIRouter()
@router.post("/user/auth/login", response_model = UserResponse, status_code=status.HTTP_200_OK)
def login_user(response: Response,
               data:UserLoginDTO,
               service: AuthService = Depends(get_auth_service)):
    user_data = service.login_user(data)
    response.set_cookie(
        key="access_token",
        value=user_data.access_token,
        httponly=True
    )
    response.set_cookie(
        key="refresh_token",
        value=user_data.refresh_token,
        httponly=True
    )
    return user_data.user

@router.post("/user/auth/refresh", status_code=status.HTTP_200_OK)
def token_refresh(response: Response,
                  user: User = Depends(get_current_user_from_refresh)):
    token = jwt_service.refresh_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True)
    return
