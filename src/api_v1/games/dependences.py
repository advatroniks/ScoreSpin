from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.models import db_helper, Game
from . import crud


async def get_game_by_id(
        game_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
) -> Game:
    game = await crud.get_game_by_id(session=session, game_id=game_id)

    if game:
        return game
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Pizdec, idi nahui ebanij pidor"
    )



