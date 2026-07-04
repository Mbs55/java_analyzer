from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
@app.get("/")
def root():
    return {"health":"ok"}

@app.get("/items/{id}")
def test():
    return {"id":id}
