from src.api_v1.games.schemas import GameCreate
from sqlalchemy import select
from src.models import Profile
from sqlalchemy.ext.asyncio import AsyncSession

'''
    Изменение (дельта) RTTF-рейтинга после одной встречи = [(100 - (PВ - PП)) / 10]  * k * D, 

    где РВ - рейтинг выигравшего, РП - рейтинг проигравшего, k - коэффициент турнира, D - коэффициент счета.

    Если РВ на 100 и более превышает РП, то дельта = 0 

    Рейтинг не может опуститься ниже 1.
'''
async def calculateRating(
        game: GameCreate,
        session: AsyncSession
) -> dict:



    stmt = select(Profile).where(Profile.user_id == game.winner_id)
    result = await session.execute(statement=stmt)
    winner_profile = result.scalar_one_or_none()
    winner_rating = winner_profile.rating

    stmt = select(Profile).where(Profile.user_id == game.loser_id)
    result = await session.execute(statement=stmt)
    loser_profile = result.scalar_one_or_none()
    loser_rating = winner_profile.rating

    #коэф. счёта d зависит от разницы в счёте по итогу матча
    d = {1:0.8, 2:1, 3:1.2}[ abs(game.winner_score - game.loser_score)]


    delta = (100 - (winner_rating- loser_rating)) / 10 * d

    return {game.winner_id:delta, game.loser_id: -delta}


