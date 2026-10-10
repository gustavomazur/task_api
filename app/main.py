from fastapi import FastAPI
from .database import engine, Base
from .routers import task

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task.router)
