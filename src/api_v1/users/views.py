from fastapi import  APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import GetUserSchema, NewUserCreateSchema, PutUpdateUserSchema, PatchUpdateUserSchema
from src.models import db_helper, User
from .dependences import get_user_dependency
from src.api_v1.users.registration.schemas import UserRegistration


router = APIRouter(tags=["Users"])


from .registration.views import router as registration_router
from .user_profile.views import router as profile_router

router.include_router(registration_router, prefix="/registration")
router.include_router(profile_router, prefix="/profile")



# @router.post("/", response_model=GetUserSchema)
# async def create_new_user(
#         new_user: UserRegistration,
#         session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
# ):
#     return await crud.create_new_user(
#         new_user=new_user,
#         session=session
#     )
#
#
# @router.get("/", response_model=GetUserSchema)
# async def get_current_user(
#         user_pid: User = Depends(get_user_dependency),
#         session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
# ):
#     return user_pid
#
#
# @router.put("/", response_model=GetUserSchema)
# async def update_user(
#         user_for_update: PutUpdateUserSchema | PatchUpdateUserSchema,
#         current_user: User = Depends(get_user_dependency),
#         session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
# ):
#     return await crud.update_user(
#         session=session,
#         user_for_update=user_for_update,
#         current_user=current_user
#     )
