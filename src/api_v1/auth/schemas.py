from pydantic import BaseModel, EmailStr, Field


class AuthUserData(BaseModel):
    username: EmailStr
    password: str = Field(min_length=10, max_length=40)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str | None = None


class User(BaseModel):
    email: str
    username: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    user_role: str


class UserInDB(User):
    hashed_password: str


