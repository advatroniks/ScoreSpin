from pydantic import BaseModel, ValidationError, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserModel(BaseModel):
    password1: str
    password2: str

    @field_validator("password2")
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        print(info.data)

UserModel(password1="abc", password2="abc")

