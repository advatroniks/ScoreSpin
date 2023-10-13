import uuid
from typing import Literal

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, db_helper

from .serv_Tour_process import TournamentEngine


class Tournament:
    def __init__(
            self,
            members: list[User],
            tournament_type: Literal["standard", "extend"],
            tables: list[int],
            session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
    ):
        self.members = members
        self.tournament_type = tournament_type
        self.tables = tables
        self.tour_id = uuid.uuid4()
        self.engine = TournamentEngine(self.members, self.tables)

    def add_game(self):
        self.engine.add_game()

    async def start_tournament(self):
        await self.engine.start_tournament()