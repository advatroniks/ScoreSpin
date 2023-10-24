from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserRegistration

from src.models import db_helper
from src.api_v1.users import crud
from src.api_v1.users.schemas import GetUserSchema

router = APIRouter()


@router.post(path="/", response_model=GetUserSchema)
async def registration_user(
        new_user: UserRegistration,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    user = await crud.create_new_user(
        new_user=new_user,
        session=session,
    )
    await crud.create_new_profile(user.id, session)

    return user

