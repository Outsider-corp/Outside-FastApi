import datetime
import uuid
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Depends
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

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Roman'},
    {'id': 2, 'role': 'beginner', 'name': 'Radmir'},
    {'id': 3, 'role': 'traider', 'name': 'Sgor'},
]
fake_users_2 = [
    {
        'id': 1, 'role': 'admin', 'name': 'Roman', 'degree': [{
        'id': 1, 'created_at': datetime.datetime.now(), 'type_degree': 'expert'
    }]
    },
    {
        'id': 2, 'role': 'beginner', 'name': 'Radmir',
    },
    {
        'id': 3, 'role': 'trader', 'name': 'Sgor'
    },
]

fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 25000, 'amount': 0.0023},
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 29500, 'amount': 0.0015}
]


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


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users_2 if user.get('id') == user_id]


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    curr_user = list(filter(lambda user: user.get('id') == user_id, fake_users_2))[0]
    curr_user['name'] = new_name
    return {'status': 200, 'data': curr_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trade(trade: Trade):
    fake_trades.append(trade)
    return {'status': 200, 'data': fake_trades}
