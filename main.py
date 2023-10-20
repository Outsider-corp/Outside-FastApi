from fastapi import FastAPI

app = FastAPI(
    title='Outside Crypto'
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Roman'},
    {'id': 2, 'role': 'beginner', 'name': 'Radmir'},
    {'id': 3, 'role': 'traider', 'name': 'Sgor'},
]


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]
