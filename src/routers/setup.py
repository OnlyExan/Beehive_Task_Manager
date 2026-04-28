# src/routers/setup.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src import models, schemas
from src.security.passwords import hash_password

router = APIRouter(prefix="/setup", tags=["setup"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/status")
def setup_status(db: Session = Depends(get_db)):
    """
    Returns whether setup has already been completed.
    Frontend uses this to decide whether to show the setup form or redirect.
    """
    count = db.query(models.Employee).count()
    return {"setup_complete": count > 0}


@router.post("", status_code=status.HTTP_201_CREATED)
def first_time_setup(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    """
    Creates the very first admin account.
    Only works when the employees table is completely empty.
    Locks itself permanently once any employee exists.
    """
    count = db.query(models.Employee).count()
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Setup already completed. Please log in.",
        )

    # Force role to admin regardless of what was sent in the request
    admin = models.Employee(
        full_name=employee_in.full_name,
        email=employee_in.email,
        role="admin",
        hashed_password=hash_password(employee_in.password),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "message": "Admin account created successfully. Please log in.",
        "email": admin.email,
    }