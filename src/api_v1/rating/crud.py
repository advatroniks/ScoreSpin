from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import Game


async def create_rating_game(session: AsyncSession):
    pass