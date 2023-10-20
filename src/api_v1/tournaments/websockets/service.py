from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.oauth2 import get_current_user


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


async def websocket_auth(
        websocket: WebSocket,
        session: AsyncSession,

):
    await websocket.accept()

    token = await websocket.receive_text()

    user = await get_current_user(
        token=token,
        session=session
    )

    if user:
        return user
    else:
        await websocket.close(code=4000, reason="User Unauthorized! Sosi chlen, eblo")

