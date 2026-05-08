# src/security/auth.py
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src import models
from src.security.passwords import verify_password


# ===== JWT config =====
SECRET_KEY = os.environ["SECRET_KEY"]          # pulled from .env — never hardcode this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ===== DB dependency =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===== Authentication helpers =====

def authenticate_employee(email: str, password: str, db: Session) -> models.Employee | None:
    """Return employee if email/password are valid, else None."""
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ===== Current user dependency =====

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> models.Employee:
    """Decode JWT, load employee from DB, or raise 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # sub is stored as a string — convert to int for the DB lookup
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        employee_id = int(sub)

    except (jwt.PyJWTError, ValueError):
        raise credentials_exception

    user = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if user is None:
        raise credentials_exception

    return user