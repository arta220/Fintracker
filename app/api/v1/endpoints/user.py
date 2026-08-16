
from fastapi import APIRouter, Depends, Response
from starlette import status
from app.api.v1.dependency.dependency import get_current_user, get_current_user_from_refresh, get_data_service
from app.api.v1.dependency.dependency import get_auth_service
from app.DTO.user import *
from app.service.AuthService import AuthService
from app.repository.db_models import User
from app.service.DataService import DataService

router = APIRouter()

@router.post("/user/auth/register", response_model = UserResponse, status_code=status.HTTP_201_CREATED)
def reg_user(
        response: Response,
        data:UserRegisterDTO,
        service: AuthService = Depends(get_auth_service)
):
    user_data = service.reg_user(data)

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


@router.get("/user", response_model= UserResponse, status_code=status.HTTP_200_OK)
def get_user(user = Depends(get_current_user)) -> None:
    return user

@router.patch("/user", response_model = UserResponse, status_code=status.HTTP_200_OK)
def update_username_email(data: UserUpdateDTO,
                user: User = Depends(get_current_user),
                service: AuthService = Depends(get_auth_service)) -> None:
     return service.update_user(data,user)

@router.post("/user/password",response_model= UserResponse, status_code=status.HTTP_200_OK)
def update_password(data: PasswordUpdateDTO,
        user: User = Depends(get_current_user_from_refresh),
        service:  DataService = Depends(get_data_service)):

    return service.update_password(user,data)

@router.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user = Depends(get_current_user), service: AuthService = Depends(get_auth_service)) -> None:
    service.delete_user(user)
    return

