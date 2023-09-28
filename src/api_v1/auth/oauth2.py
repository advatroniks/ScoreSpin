from datetime import datetime, timedelta
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from . import hash_password

from src.api_v1.users import crud
from src.models import db_helper, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/token")


async def authenticate_user(
        user_email: str,
        password: str,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
):
    user = await crud.get_current_user_by_email(
        session=session,
        user_email=user_email,
    )

    if not user:
        return False

    if not hash_password.verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency),
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_email=user_email)
    except JWTError:
        raise credentials_exception
    user = await crud.get_current_user_by_email(
        user_email=token_data.user_email,
        session=session
    )
    if user is None:
        raise credentials_exception
    return user



