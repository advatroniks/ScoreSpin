import uuid

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy import select

from src.models import Game, Tournament, Profile
from .schemas import GameCreate, GameUpdate, GameBase
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


async def create_game(
        session: AsyncSession,
        game_add: GameCreate,
        tournament_pid: int | None
) -> Game:
    game = Game(**game_add.model_dump())
    print(game.id)
    print(game.id, "game_id")
    session.add(game)
    print(game.id, "after")
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


async def check_player_in_tournament(
        session: AsyncSession,
        tournament_pid: int,
        profiles: list[Profile]
) -> Profile:
    stmt = (select(
        Tournament
    ).options(
        selectinload(Tournament.players_profiles)
    ).where(
        Tournament.pid == tournament_pid
    )
    )

    result_seq: Result = await session.execute(statement=stmt)

    tournament: Tournament | None = result_seq.one_or_none()
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found! "
        )

    validate_profiles: list[Profile] = []
    for profile_in_tournament in tournament.players_profiles:  # type:Profile
        if profile_in_tournament.id in [profile.id for profile in profiles]:
            validate_profiles.append(profile_in_tournament)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Player in tournament not found!!! Fuck..."
    )
