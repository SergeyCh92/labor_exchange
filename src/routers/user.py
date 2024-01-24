import logging

from fastapi import APIRouter, Depends, Response, status

from src.database.tables import User
from src.dependencies import get_current_user, get_user_service
from src.schemas import updateUserSchema, userInSchema, userSchema
from src.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


# добавил get_current_user, чтобы запретить получать данные о пользователях незарегистрированным юзерам
@router.get("/users", response_model=list[userSchema])
async def get_users(
    limit: int = 100,
    skip: int = 0,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"request was received to receive {limit} users, offset {skip}")
    results = await user_service.get_users(limit=limit, skip=skip)
    logging.info(f"{len(results)} users have been successfully received")
    return results


@router.post("/user", response_class=Response)
async def create_user(user_schema: userInSchema, user_service: UserService = Depends(get_user_service)):
    logging.info("request has been received to create a new user")
    await user_service.create_user(user_schema=user_schema)
    logging.info("the user has been successfully created")
    # у фронта уже есть все данные о пользователе (которые приложены в полезную нагрузку)
    # в связи с этим предлагаю не возвращать их, а просто отдавать код ответа, для отрисовки можно использовать данные,
    # ранее вложенные в полезную нагрузку
    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/user/{user_id}", response_class=Response)
async def update_user(
    user_id: int,
    update_user_schema: updateUserSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"a request was received to update user id {user_id} data")
    await user_service.update_user(user_id=user_id, update_user_schema=update_user_schema, current_user=current_user)
    logging.info(f"the data of the user id {user_id} has been updated")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/{user_id}", response_model=userSchema)
async def get_user(
    user_id: int, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)
):
    logging.info(f"data on the {id} id user has been requested")
    user = await user_service.get_user(user_id=user_id)
    logging.info(f"the data on the user {id} id has been received")
    return user
