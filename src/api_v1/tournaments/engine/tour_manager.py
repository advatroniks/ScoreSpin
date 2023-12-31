from typing import Literal

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, db_helper
from src.api_v1.users.crud import get_user_by_any_parameter

from .tour_engine import TournamentEngine


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
        self.tour_id = 1  # mock for tests
        self.engine = TournamentEngine(self.members, self.tables)
        self.session = session

    def add_game(self):
        self.engine.add_game()

    async def start_tournament(self):
        await self.engine.start_tournament()

    @property
    async def table_conditions(self) -> dict[int, list[User]]:
        _table_conditions = {}
        print(self.engine.table_conditions, "TEST" * 20)
        for table, pair in self.engine.table_conditions.items():
            _table_conditions[table] = []
            for user in pair:
                user = await get_user_by_any_parameter(
                    parameter="id",
                    value=user,
                    session=self.session
                )
                _table_conditions[table].append(user)

        return _table_conditions
