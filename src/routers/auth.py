# src/routers/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.security.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_employee,
    create_access_token,
)
from src import schemas

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is the endpoint OAuth2PasswordBearer points to (tokenUrl="auth/login")
# It uses form data (username + password) so FastAPI's /docs Authorize button works
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm uses "username" field — we treat it as email
    employee = authenticate_employee(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(employee.id), "role": employee.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": employee.id,
        "full_name": employee.full_name,
        "email": employee.email,
        "role": employee.role,
    }


# JSON body login — used by your HTML frontend (not the /docs form)
@router.post("/login/json")
def login_json(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    employee = authenticate_employee(
        email=credentials.email,
        password=credentials.password,
        db=db,
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={"sub": str(employee.id), "role": employee.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": employee.id,
        "full_name": employee.full_name,
        "email": employee.email,
        "role": employee.role,
    }