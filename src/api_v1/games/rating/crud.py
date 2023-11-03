from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.models import Game, Rating
from src.api_v1.games.crud import create_game


async def create_rating_transaction(
        session: AsyncSession,
        tournament_pid: int,
        profile_pid: int,
        game_pid: int,
        rating_total: int,
        rating_diff: int

):
    rating = Rating(
        tournament_pid=tournament_pid,
        profile_pid=profile_pid,
        game_pid=game_pid,
        rating_total=rating_total,
        rating_diff=rating_diff
    )

    session.add(rating)

    await session.commit()


async def get_actual_profile_rating(
        session: AsyncSession,
        profile_pid: int
) -> int | None:
    stmt = select(
        Rating
    ).where(
        Rating.profile_pid == profile_pid
    ).order_by(
        desc(Rating.rating_registrations.des)
    ).limit(1)

    result_row = await session.execute(statement=stmt)

    actual_rating: Rating | None = result_row.scalar_one_or_none()

    if not actual_rating:
        return None

    return actual_rating.rating_total


async def get_average_rating_players_in_tournament(
        session: AsyncSession
):
    pass
