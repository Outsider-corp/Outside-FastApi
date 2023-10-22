from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get('/')
def start():
    return FileResponse('test.html')


@app.post('/calculate')
def calc(num1: float, num2: float):
    return {'result': num1 + num2}
