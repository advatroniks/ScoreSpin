import asyncio
import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper

from .service_tournament.serv_Tour_buffer import TOURNAMENT_BUFFER
from .schemas import CreateTournament
from .crud import get_tournaments_members
from .service_tournament.serv_Tour_Manager import Tournament

router = APIRouter(
    tags=["Tournaments"]
)


@router.post(
    path="/create_tournament"
)
async def create_tournament(
        members_list: list[uuid.UUID],
        tables_list: list[int],
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    members = await get_tournaments_members(
        members_list=members_list,
        session=session
    )

    tournament = Tournament(
        members=members,
        tournament_type="standard",
        tables=tables_list,
        session=session
    )

    TOURNAMENT_BUFFER[1] = tournament
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", TOURNAMENT_BUFFER.get(1).members)


@router.post(
    path="/start/"
)
async def start_tournament(
        tournament_id: int
):
    print(TOURNAMENT_BUFFER)
    current_tournament = TOURNAMENT_BUFFER.get(tournament_id)
    await current_tournament.start_tournament()


@router.post(
    path="/complete_game"
)
async def complete_game(
        table_number: int
):
    current_tournament = TOURNAMENT_BUFFER.get(1)
    current_tournament.engine.table_operator.remove_game_from_table(table_number=table_number)