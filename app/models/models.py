from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = Field(gt=0)
    is_subscribed: Optional[bool] = None


class Feedback(BaseModel):
    name: str
    message: str


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class User(BaseModel):
    username: str
    password: str
