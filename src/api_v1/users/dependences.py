from . import crud
from src.models import User, db_helper
from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_dependency(
        user_pid: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
) -> User:
    user = await crud.get_current_user_by_id(user_pid=user_pid, session=session)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Eblo, you have to enter correct data. Assshole!!"
    )