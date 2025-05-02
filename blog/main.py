from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


from .schemas import Blog
app = FastAPI()



@app.post("/blog")
def create(request: Blog):
    return request