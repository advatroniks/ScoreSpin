from fastapi import APIRouter

from .games.views import router as games_router
from .users.views import router as users_router
from .auth.views import router as auth_router
from .users.registration.views import router as registration_router


router = APIRouter()

router.include_router(router=auth_router, prefix="/login")
router.include_router(router=games_router, prefix="/games")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=registration_router, prefix="/registration")


