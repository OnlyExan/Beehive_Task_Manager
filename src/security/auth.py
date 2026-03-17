# src/security/auth.py
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src import models
from src.security.passwords import verify_password 


# ===== JWT config (align these with your app’s settings) =====
SECRET_KEY = "change_me_to_a_long_random_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Token URL is the path of your login endpoint (e.g. /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ===== DB dependency =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===== Authentication helpers =====

def authenticate_employee(
    email: str,
    password: str,
    db: Session,
) -> models.Employee | None:
    """Return employee if email/password are valid, else None."""
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    if user is None:
        return None

    # uses your bcrypt-based verify_password
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        employee_id: int | None = payload.get("sub")
        if employee_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id)
        .first()
    )
    if user is None:
        raise credentials_exception

    return user
