import logging

from fastapi import APIRouter, Depends, Response, status

from src.dependencies import get_current_user, get_response_service
from src.schemas import ResponseCreateSchema, UserSchema
from src.services import ResponseService

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("/response", response_class=Response)
async def create_response(
    response_schema: ResponseCreateSchema,
    response_service: ResponseService = Depends(get_response_service),
    current_user: UserSchema = Depends(get_current_user),
):
    logging.info(f"the response creation request was received from user id {current_user.id}")
    await response_service.create_response(response_schema=response_schema, current_user=current_user)
    logging.info(f"the reponse has been created, the owner is the user id {current_user.id}")
    return Response(status_code=status.HTTP_201_CREATED)
