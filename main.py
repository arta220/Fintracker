from urllib.request import Request

from fastapi import FastAPI
from jwt import ExpiredSignatureError
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from app.repository.database import engine, Base
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.tags import router as tags_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.transactions import router as transactions_router
from app.api.v1.endpoints.goals import router as goals_router
from app.api.v1.endpoints.budget import router as budget_router

from fastapi.responses import JSONResponse

from app.exceptions.exceptions import *

app = FastAPI()
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])
app.include_router(tags_router, prefix="/api/v1", tags=["tags"])
app.include_router(transactions_router, prefix="/api/v1", tags=["transactions"])
app.include_router(goals_router, prefix="/api/v1", tags=["goals"])
app.include_router(budget_router, prefix="/api/v1", tags=["budget"])


@app.get("/")
def root():
    return{
        "message":"Server works"
    }

@app.exception_handler(IntegrityError)
async def wrong_query_handler(
        request: Request,
        exc: IntegrityError
):
    return JSONResponse(status_code=409, content =
    {
        "detail":exc.orig.diag.message_detail
    })
@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError
):
    return JSONResponse(status_code=409, content =
    {
        "detail":"User already exists"
    })

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError
):
    return JSONResponse(status_code=404, content =
    {
        "detail":"User not found"
    })

@app.exception_handler(NoResultFound)
async def record_not_found_handler(
        request: Request,
        exc: NoResultFound
):
    return JSONResponse(status_code=404, content =
    {
        "detail":"Record not found"
    })


@app.exception_handler(WrongPasswordError)
async def wrong_password_handler(
        request: Request,
        exc: WrongPasswordError
):
    return JSONResponse(status_code=401, content =
    {
        "detail":"Wrong password"
    })

@app.exception_handler(ExpiredSignatureError)
async def expired_token_handler(
        request: Request,
        exc: ExpiredSignatureError
):
    return JSONResponse(status_code=401, content =
    {
        "detail":"Token has expired"
    })

@app.exception_handler(InvalidToken)
async def invalid_token_handler(
        request: Request,
        exc: InvalidToken
):
    return JSONResponse(status_code=401, content =
    {
        "detail":"Invalid token"
    })

@app.exception_handler(AppError)
async def app_error_handler(
    request: Request,
    exc: AppError
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Server died: {exc.orig.diag.message_detail}"
        }
    )


Base.metadata.create_all(bind=engine)
