# src/routers/employees.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models, schemas
from src.security.passwords import hash_password
from src.security.roles import require_roles

router = APIRouter(prefix="/employees", tags=["employees"])

VALID_ROLES = {"admin", "employee"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    # Validate role is one of the allowed values
    if employee_in.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(VALID_ROLES)}",
        )

    existing = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    employee = models.Employee(
        full_name=employee_in.full_name,
        email=employee_in.email,
        role=employee_in.role,
        hashed_password=hash_password(employee_in.password),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("", response_model=list[schemas.EmployeeRead])
def list_employees(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return db.query(models.Employee).all()


@router.get("/{employee_id}", response_model=schemas.EmployeeRead)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    # Validate role if it's being changed
    if employee_in.role is not None and employee_in.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(VALID_ROLES)}",
        )

    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    if employee_in.full_name is not None:
        employee.full_name = employee_in.full_name
    if employee_in.email is not None:
        employee.email = employee_in.email
    if employee_in.role is not None:
        employee.role = employee_in.role

    db.commit()
    db.refresh(employee)
    return employee