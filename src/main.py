# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeeHive TTM API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "TTM API is running"}


@app.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()
