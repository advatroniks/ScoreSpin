from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper

from .oauth2 import authenticate_user, create_access_token, get_current_user
from .schemas import Token, User


router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=Token, status_code=status.HTTP_202_ACCEPTED)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    user = await authenticate_user(
        user_email=form_data.username,
        password=form_data.password,
        session=session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user



