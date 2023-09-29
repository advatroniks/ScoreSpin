from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.models import Game
from .schemas import GameCreate, GameUpdate, GameUpdatePartial


async def get_game(session: AsyncSession) -> list[Game]:
    stmt = select(Game, Game.id).order_by(Game.id)
    result: Result = await session.execute(stmt)
    games = result.scalars().all()
    return list(games)


async def get_game_by_id(session: AsyncSession, game_id: int) -> Game | None:
    return await session.get(Game, game_id)


async def create_game(session: AsyncSession, game_add: GameCreate) -> Game:
    game = Game(**game_add.model_dump())
    print(game.id)
    session.add(game)
    await session.commit()
    return game


async def update_game(
        session: AsyncSession,
        game: Game,
        game_update: GameUpdate | GameUpdatePartial,
        partial=False
) -> Game:
    for name, value in game_update.model_dump(exclude_unset=partial).items():
        setattr(game, name, value)
    await session.commit()
    return game


async def delete_game(
        session: AsyncSession,
        game: Game
) -> None:
    await session.delete(game)
    await session.commit()
