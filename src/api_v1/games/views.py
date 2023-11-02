from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .dependences import get_game_by_id
from . import crud
from .schemas import Game, GameCreate, GameUpdate
from src.models import db_helper

from .service import validate_game

from src.api_v1.auth.authorization import super_admin_access, moderator_access, user_access


router = APIRouter(tags=["Games"])


@router.post(
    path="/",
    response_model=Game,
    dependencies=[Depends(user_access)],
    status_code=status.HTTP_201_CREATED
)
async def create_game(
        game_add: GameCreate,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    await validate_game(
        **game_add.__dict__,
        session=session,
        winner_player_id=game_add.winner_player_id,
    )
    print('hello world' * 20)
    return await crud.create_game(session=session, game_add=game_add)


@router.get(
    path="/",
    response_model=list[Game]
)
async def get_game(
        game_count: int | None = 10,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    return await crud.get_games(
        game_count=game_count,
        session=session
    )


@router.get(
    path="/{game_id}",
    response_model=Game
)
async def get_game_by_id(
        game: Game = Depends(get_game_by_id)
) -> Game:
    return game


@router.patch("/{game_id}")
async def update_game_partial(
        game_update: GameUpdate,
        game: Game = Depends(get_game_by_id),
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    return await crud.update_game(
        session=session,
        game_update=game_update,
        game=game,
        partial=True
    )


@router.delete("/{game_id}")
async def delete_game(
        game: Game = Depends(get_game_by_id),
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
) -> None:
    await crud.delete_game(session=session, game=game)
