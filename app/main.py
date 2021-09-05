from fastapi import FastAPI

from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
def index():
    return {"data": {"name": "Mofe"}}


@app.get("/about")
def about():
    return {"data": {"about": "page"}}


@app.get("/blog/{id}")
def show(id):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id):
    return {"data": {"1", "2"}}
