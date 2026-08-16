from typing import Generator

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from app.repository.db_manager import DbManager
from app.repository.database import SessionLocal
from app.repository.db_models import User
from app.service.AuthService import AuthService
from app.repository.jwt import decode_token
from app.exceptions.exceptions import *
from app.service.DataService import DataService


#в fastapi важен порядок методов. идет сверху вниз, поэтому вызываемые методы должны быть выше
#как и с ручками, где /auth/me и /auth/{id} могут иметь разное обращение, а могут не иметь
def get_db() -> Generator[Session, None, None]:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_manager(db: Session = Depends(get_db)) -> DbManager:
    return DbManager(db)

def get_auth_service(db_manager: DbManager = Depends(get_manager)) -> AuthService:
    return AuthService(db_manager)

def get_data_service(db_manager: DbManager = Depends(get_manager)) -> DataService:
    return DataService(db_manager)


def get_token_payload(token: str) -> dict:
    payload = decode_token(token)
    # гига-умный мув: преобразуем sub в инт
    # и сразу ловим: отсутствие ключа, не тот тип
    # и обощаем в InvalidTokenError
    try:
        int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise InvalidTokenError

    return payload


def get_access_token_payload(
    token: str | None = Cookie(default=None, alias = "access_token")
) -> dict:
    if token is None:
        raise InvalidTokenError
    payload = get_token_payload(token)
    if payload.get("type") != "access":
        raise InvalidTokenError

    return payload


def get_refresh_token_payload(
        token: str | None = Cookie(default=None, alias = "refresh_token")
) -> dict:
    if token is None:
        raise InvalidTokenError
    payload = get_token_payload(token)
    if payload.get("type") != "refresh":
        raise InvalidTokenError
    return payload


def find_user_by_payload(
    payload: dict,
    db_manager: DbManager
) -> User:
    user_id = int(payload["sub"])
    user = db_manager.get_record(
        User,
        {"id" : user_id}
    )
    #рудимент?
    if user is None:
        raise UserNotFoundError
    return user

def get_current_user(
    payload: dict = Depends(get_access_token_payload),
    db_manager: DbManager = Depends(get_manager)
) -> User:
    return find_user_by_payload(payload, db_manager)

def get_current_user_from_refresh(
    payload: dict = Depends(get_refresh_token_payload),
    db_manager: DbManager = Depends(get_manager)
) -> User:
    return find_user_by_payload(payload, db_manager)

