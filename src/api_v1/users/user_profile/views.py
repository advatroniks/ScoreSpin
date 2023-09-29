from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.users import crud
from src.api_v1.users.schemas import GetUserSchema, PatchUpdateUserSchema
from src.models import User, db_helper
from src.api_v1.auth.oauth2 import get_current_user
from src.api_v1.auth.authorization import super_admin_access


router = APIRouter()


@router.patch(
    path="/update_profile",
    response_model=GetUserSchema,
    dependencies=[Depends(super_admin_access)]
)
async def update_profile(
    user_for_update: PatchUpdateUserSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user_for_update=user_for_update,
        current_user=current_user
    )

