import asyncio
import uuid
import json

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


from src.models import db_helper
from src.api_v1.users.crud import get_current_user_by_pid
from src.api_v1.tournaments.service_tournament.Tour_connect_manager import connection_manager
from src.api_v1.tournaments.service_tournament.Tour_Buffer import ACTIVE_TOURNAMENTS
from .service import CheckForAccessConnect


router = APIRouter(tags=["WebSocketTesting"])

#'ws://localhost:8000/api/v1/test_websocket/ws/${currentRoom}/${user}


templates = Jinja2Templates(directory="templates")


connections_list: list[WebSocket] = []


@router.get(path='/')
async def get_html(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@router.websocket(path='/ws/{tournament_id}/{user_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        tournament_id: int,
        user_id: int
):
    check_access = CheckForAccessConnect(
        tournament_id=tournament_id,
        user_pid=user_id,
        active_tournaments=ACTIVE_TOURNAMENTS
    )

    if check_access.tournament:
        await connection_manager.connect(
            websocket=websocket,
            tournament_id=tournament_id,
            user_id=user_id
        )

    while True:
        data = await websocket.receive_json()
        print(data)
        if "start_tournament" in data:
            await asyncio.create_task(ACTIVE_TOURNAMENTS[tournament_id].start_tournament())
        if "result" in data:
            ACTIVE_TOURNAMENTS[tournament_id].engine.table_operator.remove_game_from_table(int(data['result']))

        await asyncio.sleep(5)

        tables_conditions = await ACTIVE_TOURNAMENTS[tournament_id].table_conditions

        for key in tables_conditions:
            tables_conditions[key][0] = tables_conditions[key][0].first_name + ' ' + tables_conditions[key][0].surname
            tables_conditions[key][1] = tables_conditions[key][1].first_name + ' ' + tables_conditions[key][1].surname

        await websocket.send_json(tables_conditions)