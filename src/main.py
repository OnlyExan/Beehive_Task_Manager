# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .routers import employees

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeeHive TTM API")
app.include_router(employees.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "TTM API is running"}