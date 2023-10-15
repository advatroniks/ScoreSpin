import asyncio
import uuid


from sqlalchemy.ext.asyncio import  AsyncSession
from fastapi import Depends

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


from src.models import db_helper
from src.api_v1.users.crud import get_current_user_by_pid
from src.api_v1.tournaments.service_tournament.Tour_Manager import Tournament
from src.api_v1.tournaments.service_tournament.Tour_Buffer import TOURNAMENT_BUFFER

router = APIRouter(tags=["WebSocketTesting"])

#'ws://localhost:8000/api/v1/test_websocket/ws/${currentRoom}/${user}'


html ="""
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Example</title>
</head>
<body>
    <div>
        <input id="userIdInput" type="text" placeholder="Введите user_id">
        <button id="setUserIdButton">Установить user_id</button>
    </div>
    <div>
        <button id="connectButton" disabled>Соединиться</button>
        <button id="finishMatchButton" disabled>Завершить матч</button>
        <select id="matchResult" disabled>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
        </select>
    </div>
    <div id="serverResponse"></div>

    <script>
        const userIdInput = document.getElementById('userIdInput');
        const setUserIdButton = document.getElementById('setUserIdButton');
        const connectButton = document.getElementById('connectButton');
        const finishMatchButton = document.getElementById('finishMatchButton');
        const matchResult = document.getElementById('matchResult');
        const serverResponse = document.getElementById('serverResponse');
        let ws;
        let userId; // Переменная для хранения user_id
        let tournamentId; // Переменная для хранения tournament_id

        setUserIdButton.addEventListener('click', () => {
            // Установка user_id и активация кнопок
            userId = userIdInput.value;
            tournamentId = 1; // Номер турнира по умолчанию
            if (userId) {
                userIdInput.setAttribute('disabled', true);
                setUserIdButton.setAttribute('disabled', true);
                connectButton.removeAttribute('disabled');
                finishMatchButton.removeAttribute('disabled');
                matchResult.removeAttribute('disabled');
            }
        });

        connectButton.addEventListener('click', () => {
            if (userId) {
                // Подключение к WebSocket серверу и передача user_id и tournament_id
                ws = new WebSocket(`ws://localhost:8000/api/v1/test_websocket/ws/${tournamentId}/${userId}`);
                ws.onopen = () => {
                    console.log('WebSocket соединение установлено.');
                };
                ws.onmessage = (event) => {
                    // Отображение JSON-ответа от сервера
                    const response = JSON.parse(event.data);
                    serverResponse.textContent = JSON.stringify(response, null, 2);
                };
            }
        });

        finishMatchButton.addEventListener('click', () => {
            if (userId) {
                // Отправка информации о завершении матча
                const result = matchResult.value;
                const data = {
                    user_id: userId,
                    tournament_id: tournamentId,
                    result: result
                };
                ws.send(JSON.stringify(data));
            }
        });
    </script>
</body>
</html>

"""


connections_list: list[WebSocket] = []


@router.get(path='/')
async def get_html():
    print(id(TOURNAMENT_BUFFER))

    return HTMLResponse(content=html)


@router.websocket(path='/ws/{tournament_id}/{user_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        tournament_id: int,
        user_id: int,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    for tournament in TOURNAMENT_BUFFER:
        print(tournament, tournament_id)
        if tournament == tournament_id:
            user = await get_current_user_by_pid(user_id, session)
            for user_seq in TOURNAMENT_BUFFER[tournament_id].members:
                if user.id == user_seq.id:
                    await websocket.accept()
                    asyncio.create_task(TOURNAMENT_BUFFER[tournament].start_tournament())

    print("hey")

    while True:
        data = await websocket.receive_json()
        TOURNAMENT_BUFFER[tournament_id].engine.table_operator.remove_game_from_table(int(data['result']))
