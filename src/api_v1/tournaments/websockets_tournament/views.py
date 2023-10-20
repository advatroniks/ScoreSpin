import asyncio

from typing import Annotated

from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Request,
    Depends,
)

from src.api_v1.auth.oauth2 import get_current_user
from src.api_v1.tournaments.service_tournament.Tour_connect_manager import connection_manager
from src.api_v1.tournaments.service_tournament.Tour_Buffer import ACTIVE_TOURNAMENTS
from src.models import db_helper
from .service import CheckForAccessConnect


router = APIRouter(tags=["WebSocketTesting"])

# 'ws://localhost:8000/api/v1/test_websocket/ws/${currentRoom}/${user}


templates = Jinja2Templates(directory="templates")

connections_list: list[WebSocket] = []


@router.get(path='/')
async def get_html(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@router.websocket(
    path='/ws/{tournament_id}'
)
async def websocket_endpoint(
        websocket: WebSocket,
        tournament_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):

    await websocket.accept()
    token = await websocket.receive_text()
    print(token)

    user = await get_current_user(
        token=token,
        session=session
    )

    print(user)

    if user:
        check_access = CheckForAccessConnect(
            tournament_id=tournament_id,
            user_pid=user.pid,
            active_tournaments=ACTIVE_TOURNAMENTS
        )

        if check_access.tournament:
            await connection_manager.connect(
                websocket=websocket,
                tournament_id=tournament_id,
                user_id=user.pid
            )
            try:
                while True:
                    data = await websocket.receive_json()
                    print(data)
                    if "start_tournament" in data:
                        await asyncio.create_task(ACTIVE_TOURNAMENTS[tournament_id].start_tournament())
                    if "result" in data:
                        ACTIVE_TOURNAMENTS[tournament_id].engine.table_operator.remove_game_from_table(int(data['result']))
                        await asyncio.sleep(5)
                        tables_conditions = await ACTIVE_TOURNAMENTS[tournament_id].table_conditions

                        data_serialize = {}
                        for key, value in tables_conditions.items():
                            data_serialize[key] = [i.first_name for i in value]

                        await connection_manager.update_table_conditions_for_all_users(
                            tournament_id=tournament_id,
                            table_conditions=tables_conditions
                        )
            except WebSocketDisconnect:
                connection_manager.disconnect(
                    websocket=websocket,
                    tournament_id=tournament_id,
                    user_id=user.pid
                )

        else:
            await websocket.close(code=4000, reason="Tournament not found")

    else:
        await websocket.close(code=4000, reason="User Unauthorized")