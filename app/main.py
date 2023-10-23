import uvicorn
from fastapi import FastAPI

from models.models import Feedback
from models.models import User

app = FastAPI()

user = User(id=1, name='John Doe', age=18)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Roman'},
    {'id': 2, 'role': 'beginner', 'name': 'Radmir'},
    {'id': 3, 'role': 'traider', 'name': 'Sgor'},
]
feedbacks = []


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


@app.post('/user')
def check_user_age(user_info: User):
    ans = user_info.model_dump()
    ans.update({'is_adult': user_info.age >= 18})
    return ans


@app.post('/feedback', response_model=Feedback)
def send_feedback(feedback: Feedback):
    feedbacks.append(feedback.model_dump())
    return feedback

# if __name__ == '__main__':
#     uvicorn.run('main:app', host='localhost', port=8000, reload=True, workers=3)
