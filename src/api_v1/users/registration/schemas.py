from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date


class UserRegistration(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    username: str
    hashed_password: str = Field(..., alias='password')

    @field_validator("hashed_password")
    @classmethod
    def valid_password(cls, password):
        if len(password) <= 10:
            raise ValueError("Password length to short!")
        return password
