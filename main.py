from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def main():
    return 'Hello World'

@app.post('/')  
def main():
    return 'Hello World'
