from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import JWTBearer
from src.dependencies.database import get_session
from src.queries import user as user_queries
from src.schemas import UserSchema


async def get_current_user(
    session: AsyncSession = Depends(get_session), token_data: str = Depends(JWTBearer())
) -> UserSchema:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    if token_data is None:
        raise cred_exception
    email: str = token_data.get("sub")
    if email is None:
        raise cred_exception
    user = await user_queries.get_by_email(session=session, email=email)
    if user is None:
        raise cred_exception
    return UserSchema.from_orm(user)
