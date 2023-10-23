from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    age: int = Field(gt=0)


class Feedback(BaseModel):
    name: str
    message: str
