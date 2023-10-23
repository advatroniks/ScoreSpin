import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_
from sqlalchemy.orm.state import InstanceState

from fastapi import HTTPException, status

from src.models import User


async def validate_game(
        winner_score: int,
        loser_score: int,
        winner_id: uuid.UUID,
        loser_id: uuid.UUID,
        session: AsyncSession,
        **kwargs
):

    if winner_id == loser_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="First player equal second player! "
        )

    if winner_score == loser_score:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="First player score equal second player score! "
        )

    available_score = [score for score in range(4)]

    if winner_score not in available_score and loser_score not in available_score:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect game score. Try again pls, and fuck yourself!"
        )

    stmt = select(User).where(
        or_(
            User.id == winner_id,
            User.id == loser_id
        )
    )

    players_result_for_check = await session.execute(stmt)
    result = players_result_for_check.scalars().all()

    if len(result) != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not found user! Enter correct data!"
        )





