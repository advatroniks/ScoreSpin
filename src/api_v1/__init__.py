from fastapi import APIRouter

from .games.views import router as games_router
from .users.views import router as users_router
from .auth.views import router as auth_router
from .tournaments.views import router as tournament_router

from .tournaments.websockets_tournament.views import router as test_socket_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/login")
router.include_router(router=games_router, prefix="/games")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=tournament_router, prefix="/tournaments")
router.include_router(router=test_socket_router, prefix="/test_websocket")



