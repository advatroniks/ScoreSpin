from typing import Annotated, Literal

from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import EmailStr

from src.models import User
from .schemas import PutUpdateUserSchema, PatchUpdateUserSchema
from src.api_v1.users.registration.schemas import UserRegistration

from src.api_v1.auth.hash_password import get_password_hash


async def create_new_user(new_user: UserRegistration, session: AsyncSession) -> User:
    new_user.hashed_password = get_password_hash(new_user.hashed_password)
    user = User(**new_user.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_current_user_by_pid(user_pid: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_pid)


async def _get_user_by_any_parameter(
        parameter: Literal["pid", "first_name", "email", "username"],
        value: str,
        session: AsyncSession,
) -> User:
    condition = f"{parameter}='{value}'"
    stmt = select(User).where(text(condition))
    result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def get_current_user_by_email(
        user_email: EmailStr,
        session: AsyncSession,
) -> User | None:
    stmt = select(User).where(User.email == user_email)
    result = await session.execute(statement=stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def update_user(
        session: AsyncSession,
        user_for_update: PatchUpdateUserSchema | PutUpdateUserSchema,
        current_user: User,
        partial=False
) -> User:
    for name, value in user_for_update.model_dump(exclude_unset=partial).items():
        setattr(current_user, name, value)

    await session.commit()
    return current_user


async def delete_user(
        session: AsyncSession,
        user_for_delete: User,
):
    user_for_delete.is_active = False
    await session.commit()