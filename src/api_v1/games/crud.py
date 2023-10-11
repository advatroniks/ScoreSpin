import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select

from src.models import Game
from .schemas import GameCreate, GameUpdate
from .service import validate_game


async def get_games(
        session: AsyncSession,
        game_count: int | None = 10,
) -> list[Game]:
    stmt = select(Game, Game.id).order_by(Game.id).limit(game_count)
    result: Result = await session.execute(stmt)
    games = result.scalars().all()
    return list(games)


async def get_game_by_id(session: AsyncSession, game_id: uuid.UUID) -> Game | None:
    stmt = select(Game).where(Game.id == game_id)
    result = await session.execute(stmt)

    game: Game | None = result.scalar_one_or_none()

    return game


async def create_game(session: AsyncSession, game_add: GameCreate) -> Game:
    game = Game(**game_add.model_dump())
    print(game.id)
    session.add(game)
    await session.commit()
    return game


async def update_game(
        session: AsyncSession,
        game: Game,
        game_update: GameUpdate,
        partial=False
) -> Game:
    for name, value in game_update.model_dump(exclude_unset=partial).items():
        setattr(game, name, value)
    print(game.__dict__)
    await validate_game(
        **game.__dict__,
        session=session
    )

    await session.commit()
    return game


async def delete_game(
        session: AsyncSession,
        game: Game
) -> None:
    await session.delete(game)
    await session.commit()
