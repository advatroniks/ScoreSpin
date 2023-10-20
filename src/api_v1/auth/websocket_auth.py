from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession

from .oauth2 import get_current_user


async def websocket_auth(
        websocket: WebSocket,
        session: AsyncSession,

):
    await websocket.accept()

    token = await websocket.receive_text()

    print(token)
    user = await get_current_user(
        token=token,
        session=session,
        websocket=websocket
    )

    print(user)

    if user:
        return user
    else:
        await websocket.close(code=4000, reason="User Unauthorized! Sosi chlen, eblo")
