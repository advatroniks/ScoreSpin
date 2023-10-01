import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import or_

from fastapi import HTTPException, status

from src.models import User


async def validate_game(
        first_player_score: int,
        second_player_score: int,
        first_player_id: uuid.UUID,
        second_player_id: uuid.UUID,
        winner_id: uuid.UUID,
        session: AsyncSession
):
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Incorrect data"
    )

    if first_player_id == second_player_id:
        raise exception

    if first_player_score == second_player_score:
        raise exception

    if winner_id != first_player_id or winner_id != second_player_id:
        raise exception

    if first_player_score < second_player_score and first_player_id != winner_id:
        raise exception

    available_score = [score for score in range(4)]
    if first_player_score not in available_score and second_player_score not in available_score:
        raise exception

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





