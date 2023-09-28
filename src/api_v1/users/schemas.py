from pydantic import BaseModel, ConfigDict, UUID4, EmailStr
from typing import Annotated
from annotated_types import Ge, Gt, Le, Lt


class UserSchemaBase(BaseModel):
    first_name: str
    surname: str
    age: int
    city: str


class NewUserCreateSchema(UserSchemaBase):
    username: str
    hashed_password: str
    email: EmailStr


class GetUserSchema(UserSchemaBase):
    model_config = ConfigDict(from_attributes=True) # Sqlalchemy model >> pydantic model(get property from attributes)
    id: UUID4


class PatchUpdateUserSchema(UserSchemaBase):
    first_name: str | None = None
    surname: str | None = None
    age: int | None = None
    city: str | None = None


class PutUpdateUserSchema(UserSchemaBase):
    pass