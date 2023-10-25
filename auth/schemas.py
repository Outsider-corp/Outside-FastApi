import datetime
import uuid
from typing import Optional

from fastapi_users import schemas, models
from fastapi_users.schemas import PYDANTIC_V2
from pydantic import EmailStr, ConfigDict
from sqlalchemy import TIMESTAMP


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: models.ID
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role_id: int

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    role_id: int


class UserUpgrade(schemas.BaseUserUpdate):
    username: str
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    role_id: int
