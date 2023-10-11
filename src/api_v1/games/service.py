import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_
from sqlalchemy.orm.state import InstanceState

from fastapi import HTTPException, status

from src.models import User


async def validate_game(
        first_player_score: int,
        second_player_score: int,
        first_player_id: uuid.UUID,
        second_player_id: uuid.UUID,
        winner_id: uuid.UUID | Any,
        session: AsyncSession,
        **kwargs
):

    if first_player_id == second_player_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="First player equal second player! "
        )

    if first_player_score == second_player_score:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="First player score equal second player score! "
        )

    if winner_id not in [first_player_id, second_player_id]:
        raise ValueError("Winner_id defined incorrect! Being")

    if first_player_score > second_player_score and first_player_id != winner_id:
        raise ValueError("Winner_id defined incorrect!")

    available_score = [score for score in range(4)]
    if first_player_score not in available_score and second_player_score not in available_score:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect game score. Try again pls, and fuck yourself!"
        )

    stmt = select(User).where(
        or_(
            User.id == first_player_id,
            User.id == second_player_id
        )
    )

    players_result_for_check = await session.execute(stmt)
    result = players_result_for_check.scalars().all()
    if len(result) != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not found user! Enter correct data!"
        )





