from fastapi import FastAPI
from .db import models
from .db.database import create_db_and_tables, engine
from .routers import user, todos

app = FastAPI()

app.include_router(user.router)
app.include_router(todos.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
