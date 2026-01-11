from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class User(BaseModel):
    id: int
    name: str
    description: str

@app.get('/')
def main():
    return 'Hello World'

@app.post('/')  
def main():
    return 'Hello World'

@app.put('/')
def main():
    return 'This is put request'

