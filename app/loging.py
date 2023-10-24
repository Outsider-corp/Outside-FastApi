import json
import os
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, Cookie, Response, HTTPException
from fastapi.params import Form
from sqlalchemy import UUID
from sqlalchemy.engine import create_engine
from fastapi.responses import JSONResponse

from models.models import User

load_dotenv()
app = FastAPI()

sessions: dict = {}
users_db: Dict[int, User] = {1: User(username='admin', password='admin12345')}


def hash_pass(password: str):
    return ''.join([chr(ord(i) // 2) for i in password])


@app.post('/login')
async def login(response: Response, username: str = Form(), password: str = Form()):
    user_pass = hash_pass(password)
    for acc in users_db.values():
        if acc.username == username and acc.password == user_pass:
            session_token = 'IOJE12IOEJO'
            sessions[session_token] = username
            response.set_cookie(key=session_token, value=session_token, httponly=True)
            return {'message': 'cookies are uploaded.'}
    return {'message': 'Invalid username of password.'}


@app.post('/register')
async def register(username: str = Form(), password: str = Form()):
    if username not in [user.username for user in users_db.values()]:
        hashed_pass = hash_pass(password)
        users_db[len(users_db)] = User(username=username, password=hashed_pass)
        response = JSONResponse({'message': f'User {username} was added.'})
        response.set_cookie(key='session_token', value='2we21okoe', httponly=True)
        return response
    raise HTTPException(status_code=401, detail=f'User {username} is already exists.')


@app.get('/users')
async def users():
    return {'users': users_db}
