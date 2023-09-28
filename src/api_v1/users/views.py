from fastapi import  APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import GetUserSchema, NewUserCreateSchema, PutUpdateUserSchema, PatchUpdateUserSchema
from src.models import db_helper, User
from .dependences import get_user_dependency

router = APIRouter(tags=["Users"])


@router.post("/", response_model=GetUserSchema)
async def create_new_user(
        new_user: NewUserCreateSchema,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    return await crud.create_new_user(
        new_user=new_user,
        session=session
    )


@router.get("/{user_id}", response_model=GetUserSchema)
async def get_current_user(
        user_pid: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    return await crud.get_current_user_by_id(
        user_pid=user_pid,
        session=session
    )


@router.put("/", response_model=GetUserSchema)
async def update_user(
        user_for_update: PutUpdateUserSchema | PatchUpdateUserSchema,
        current_user: User = Depends(get_user_dependency),
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user_for_update=user_for_update,
        current_user=current_user
    )
