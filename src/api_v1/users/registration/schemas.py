from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date


class UserRegistration(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    username: str
    date_of_birth: date
    city: str
    hashed_password: str = Field(..., alias='password')

    # @field_validator("age")
    # def valid_age(cls, age):
    #     if 3 <= age <= 100:
    #         return age
    #     raise ValueError("Age not correct!")

    @field_validator("hashed_password")
    def valid_password(cls, password):
        if len(password) <= 10:
            raise ValueError("Password length to short!")
        return password
