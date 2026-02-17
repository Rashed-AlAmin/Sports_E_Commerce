from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)