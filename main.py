import datetime
import re
import uuid
from enum import Enum
from typing import List, Optional, Dict

from fastapi import FastAPI, Depends, Header, Response, Request, HTTPException
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field

from auth.database import User
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title='Outside Crypto'
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

current_user = fastapi_users.current_user()


@app.get('/protected-route')
def protected_route(user: User = Depends(current_user)):
    return f'Hello, {user.username}.'


@app.get('/unprotected-route')
def protected_route():
    return f'Hello, Noname.'


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime.datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


def check_headers(header):
    if 'User-Agent' not in header:
        raise HTTPException(status_code=400, detail='User-Agent header not found')
    if 'Accept-Language' not in header:
        raise HTTPException(status_code=400, detail='Accept-Language header not found')
    if header['Accept-Language'] not in ['en-US', 'ru-RU', 'ua-UA']:
        raise HTTPException(status_code=400, detail='Accept-Language is not in the correct format')


@app.get('/headers')
def headers(request: Request):
    header = request.headers
    check_headers(header)
    return {'User-Agent': header['User-Agent'],
            'Accept-Language': header['Accept-Language']}


@app.get('/')
def root():
    return Response(content='Hey, everyone!', media_type='text/plain',
                    headers={"Secret-Code": '24022022'})


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float
