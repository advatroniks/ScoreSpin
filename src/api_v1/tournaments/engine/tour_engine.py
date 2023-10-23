import asyncio
import uuid
from itertools import combinations

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.api_v1.games.crud import create_game
from src.api_v1.games.schemas import GameCreate
from src.api_v1.tournaments.engine.tour_connect_manager import connection_manager

from .tour_game_iter import IterationGames


def create_game_combinations(members: list[User]):
    """
    Function for create pairs players in tournament.
    :param members: User object list.
    :returns: List[(user.id: UUID, user.id: UUID), ...]
    """
    game_list = []
    for user in combinations(members, 2):
        game_list.append(
            [user[0].id, user[1].id]
        )

    return game_list


class TableOperator:
    """
    Class for distribution players for tables
    """

    def __init__(
            self,
            tables: int | list[int],
            game_list: list
    ):
        self.game_list = game_list

        if isinstance(tables, int):
            self.tables = [i for i in range(1, tables + 1)]
        if isinstance(tables, list):
            self.tables = tables

        self.table_conditions = self.get_start_table_conditions()

    def get_start_table_conditions(self):
        tables_conditions = {}
        for i in self.tables:
            tables_conditions[i] = None
        return tables_conditions

    def get_free_table(self):                                                                # PASSED
        for table, game in self.table_conditions.items():
            if game is None:
                return table, game
        return False

    def add_game_on_table(
            self,
            game: list[uuid.UUID, uuid.UUID]
    ):
        for key, value in self.table_conditions.items():
            print(key, value)
            if value is None:
                self.table_conditions[key] = game
                print(self.table_conditions)
                return True

        raise Exception("No free tables")

    def remove_game_from_table(                                                                 # PASSED
            self,
            table_number: int
    ):
        self.game_list.remove(self.table_conditions[table_number])
        self.table_conditions[table_number] = None
        print("Game removed from table number -- ", table_number)


class TournamentEngine:
    """
    При инициализации распределяются все по столам, получаем объект столов(словарь)
    """

    def __init__(
            self,
            members: list[User],
            tables: list[int]
    ):
        self.tables = tables
        self.game_list = create_game_combinations(members=members)
        self.table_operator = TableOperator(
            tables=tables,
            game_list=self.game_list
        )
        self.table_conditions = self.table_operator.table_conditions

    async def start_tournament(self):
        while len(self.game_list) != 0:
            await asyncio.sleep(3)
            if self.table_operator.get_free_table():
                self.add_game()
            print(self.table_conditions)
        print("TOURNAMENT ENDED")

    def add_game(self):
        print("add game start working...", "*" * 20)
        try:
            current_game = next(IterationGames(
                tables_conditions=self.table_conditions,
                game_list=self.game_list
            )
            )
            print(current_game)
            self.table_operator.add_game_on_table(game=current_game)

        except StopIteration:
            print("Not free tables")

    # async def complete_game(
    #         self,
    #         table_number: int,
    #         game: GameCreate | None,                                              #MOCK BY TESTING
    #         session: AsyncSession | None
    # ):
    #     await create_game(
    #         session=session,
    #         game_add=game
    #     )
    #
    #     self.table_conditions[table_number] = None
