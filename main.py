from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
