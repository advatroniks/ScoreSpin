from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Request,
    Depends,
)

from src.api_v1.tournaments.engine.tour_connect_manager import connection_manager
from .service import CheckForAccessConnect, ClientWebsocketMessageHandler
from src.api_v1.tournaments.engine.tour_buffer import ACTIVE_TOURNAMENTS
from src.api_v1.auth.websocket_auth import websocket_auth
from src.models import db_helper


router = APIRouter(tags=["WebSocketTesting"])


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

    user = await websocket_auth(websocket=websocket, session=session)

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
                    websocket_data_handler = ClientWebsocketMessageHandler(
                        websocket=websocket,
                        tournament_id=tournament_id
                    )
                    await websocket_data_handler.data_handler()

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