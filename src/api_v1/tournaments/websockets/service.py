import asyncio

from fastapi import WebSocket

from src.api_v1.tournaments.engine.tour_buffer import ACTIVE_TOURNAMENTS
from src.api_v1.tournaments.engine.tour_connect_manager import connection_manager


class CheckForAccessConnect:
    def __init__(
            self,
            tournament_id: int,
            user_pid: int,
            active_tournaments: dict
    ):
        self.user_pid = user_pid
        self.tournament_id = tournament_id
        self.tournament = self.__check_tournament_is_active(active_tournaments)

    def __check_tournament_is_active(self, active_tournaments: dict):
        for tournament_id in active_tournaments:
            print(tournament_id, active_tournaments, self.tournament_id)
            if tournament_id == self.tournament_id:
                return active_tournaments[self.tournament_id]
            else:
                return False

    def check_user_in_active_tournament(
            self
    ):
        for user in self.tournament.members:
            if user.id == self.user_pid:
                return user
            else:
                return False


class ClientWebsocketMessageHandler:
    def __init__(
            self,
            websocket: WebSocket,
            tournament_id: int
    ):
        self.websocket = websocket
        self.tournament_id = tournament_id

    async def data_handler(self):
        data = await self.websocket.receive_json()

        if "start_tournament" in data:
            await asyncio.create_task(ACTIVE_TOURNAMENTS[self.tournament_id].start_tournament())

        if "result" in data:
            ACTIVE_TOURNAMENTS[self.tournament_id].engine.table_operator.remove_game_from_table(int(data['result']))
            await asyncio.sleep(5)
            tables_conditions = await ACTIVE_TOURNAMENTS[self.tournament_id].table_conditions

            data_serialize = {}
            for key, value in tables_conditions.items():
                data_serialize[key] = [i.first_name for i in value]

            await connection_manager.update_table_conditions_for_all_users(
                tournament_id=self.tournament_id,
                table_conditions=tables_conditions
            )

