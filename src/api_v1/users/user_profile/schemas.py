from datetime import datetime

from pydantic import BaseModel, EmailStr


class ProfileAfterDelete(BaseModel):
    email: EmailStr
    deleted_time: datetime = datetime.now()
