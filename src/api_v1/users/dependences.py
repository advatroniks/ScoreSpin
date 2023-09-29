from . import crud
from src.models import User, db_helper
from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Literal


async def get_user_dependency(
        type_parameter: Literal["pid", "first_name", "email", "username"],
        value: str,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
) -> User:
    user = await crud._get_user_by_any_parameter(
        parameter=type_parameter,
        value=value,
        session=session
    )

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Eblo, you have to enter correct data. Assshole!!"
    )