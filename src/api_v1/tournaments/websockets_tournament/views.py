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

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat with Rooms</title>
</head>
<body>
    <h1>Chat with Rooms</h1>
    <div>
        <button id="room1">Tournament 1</button>
        <button id="room2">Tournament 2</button>
        <button id="room3">Room 3</button>
        <button id="room4">Room 4</button>
    </div>
    <input type="text" id="message" placeholder="Enter message please..." />
    <button id="send">Send</button>
    <div id="chat"></div>

    <script>
        const messageInput = document.getElementById('message');
        const sendButton = document.getElementById('send');
        const chat = document.getElementById('chat');
        let user;
        
        function askUserName() {
            user = prompt("Enter your name:");
            if (!user) {
                askUserName();
            }
        }
        
        askUserName();

        let socket;
        let currentRoom = 1; // Default room is 1

        function addMessage(message) {
            chat.innerHTML += message + '<br>';
        }

        function switchRoom(roomNumber) {
            currentRoom = roomNumber;
            // Close existing WebSocket connection if any
            if (socket) {
                socket.close();
            }
            socket = new WebSocket(`ws://localhost:8000/api/v1/test_websocket/ws/${currentRoom}/${user}`);
            socket.addEventListener('open', (event) => {
                console.log(`WebSocket connection opened for Room ${currentRoom}`);
            });
            socket.addEventListener('message', (event) => {
                const data = JSON.parse(event.data);
                addMessage(`${data.sender}: ${data.message}`);
            });
        }

        // Add event listeners to room buttons
        for (let i = 1; i <= 4; i++) {
            document.getElementById(`room${i}`).addEventListener('click', () => {
                switchRoom(i);
            });
        }

        sendButton.addEventListener('click', () => {
            const message = messageInput.value;
            if (message) {
                socket.send(JSON.stringify({
                    room_id: currentRoom,
                    message: message,
                    sender: user
                }));
                messageInput.value = '';
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
                    await TOURNAMENT_BUFFER[tournament].start_tournament()
                    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        await websocket.send_json(TOURNAMENT_BUFFER[tournament_id].engine.table_conditions[2])
