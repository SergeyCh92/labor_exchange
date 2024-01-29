import logging

from fastapi import APIRouter, Depends

from src.dependencies import get_auth_service
from src.schemas import LoginSchema, RefreshTokenSchema, TokenSchema
from src.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
async def login(login: LoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    logging.info(f"authentication request for the user {login.email}")
    token = await auth_service.get_token_schema(login)
    logging.info(f"user {login.email} has successfully authenticated")
    return token


@router.post("/refresh_token", response_model=TokenSchema)
async def refresh_token(refresh_token: RefreshTokenSchema, auth_service: AuthService = Depends(get_auth_service)):
    logging.info("the request for a refresh token has been received")
    token = await auth_service.refresh_token_schema(refresh_token=refresh_token.token)
    logging.info("the token has been successfully updated")
    return token
