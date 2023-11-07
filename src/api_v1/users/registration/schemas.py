from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date


class UserRegistration(BaseModel):
    first_name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=25)
    email: EmailStr
    username: str = Field(min_length=5, max_length=30)
    hashed_password: str = Field(..., alias='password')

    @field_validator("hashed_password")
    @classmethod
    def valid_password(cls, password):
        if len(password) <= 10:
            raise ValueError("Password length to short!")
        return password
