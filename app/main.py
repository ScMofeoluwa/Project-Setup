from repository.database import engine
from entity import blog_entity
from routers import blog_router
from fastapi import FastAPI

app = FastAPI()

blog_entity.Base.metadata.create_all(engine)

app.include_router(blog_router)
