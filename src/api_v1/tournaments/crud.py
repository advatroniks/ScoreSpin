import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import db_helper, User


async def get_tournaments_members(
        members_list: list[uuid.UUID],
        session: AsyncSession,
):
    users = []
    for user_id in members_list:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        users.append(user)
    print(users)
    return users




