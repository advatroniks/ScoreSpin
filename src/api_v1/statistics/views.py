from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from src.models import db_helper

router = APIRouter(tags=["Statistics"])

@router.get(
    path="/",
    response_model=list[int]
)
async def get_game(
        game_count: int | None = 10,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    return await crud.get_games(
        game_count=game_count,
        session=session
    )