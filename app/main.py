from typing import Optional, List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Form, Depends
from sqlalchemy.orm import Session

from app.database.database import session
from auth.database import get_user_db
from app.models.models import UserCreate, Feedback, Product, Man
from db_test_list import products

app = FastAPI()

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Roman'},
    {'id': 2, 'role': 'beginner', 'name': 'Radmir'},
    {'id': 3, 'role': 'traider', 'name': 'Sgor'},
]
feedbacks = []

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'message': 'Hello, World'}


@app.get('/custom')
def read_custom_message():
    return {'message': 'This is a custom message'}


@app.get('/users/{user_id}')
def is_user_exists(user_id: int):
    for user in fake_users:
        if user['id'] == user_id:
            return user
    return {'error': 'User not found'}


@app.post('/feedback', response_model=Feedback)
def send_feedback(feedback: Feedback):
    feedbacks.append(feedback.model_dump())
    return feedback


@app.post('/create_user', response_model=UserCreate)
def create_user(user: UserCreate):
    return user


@app.get('/product/{product_id}', response_model=Product)
def get_product(product_id: int):
    for prod in products:
        if prod['product_id'] == product_id:
            return Product(**prod)


@app.get('/products/search', response_model=List[Product])
def search_product(keyword: str, category: Optional[str] = None, limit: Optional[int] = 10):
    ans = []
    for prod in products:
        if keyword in prod['name']:
            if (category and prod['category'] == category) or not category:
                ans.append(Product(**prod))
    return ans[:limit]


@app.get('/login')
async def login(db: Session = Depends(get_db), username: str = Form(), password: str = Form()):
    if db.query(Man).filter((Man.username == username) & (Man.password == password)):
        return {'You got my secret, welcome'}
    else:
        return HTTPException(status_code=401, detail='Credentials ')

# if __name__ == '__main__':
#     uvicorn.run('main:app', host='localhost', port=8000, reload=True, workers=3)
