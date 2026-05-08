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
    if employee_in.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(VALID_ROLES)}",
        )

    existing = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

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
    if employee_in.role is not None and employee_in.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(VALID_ROLES)}",
        )

    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    if employee_in.full_name is not None:
        employee.full_name = employee_in.full_name
    if employee_in.email is not None:
        employee.email = employee_in.email
    if employee_in.role is not None:
        employee.role = employee_in.role

    db.commit()
    db.refresh(employee)
    return employee

@router.get("/{employee_id}/skills", response_model=list[schemas.EmployeeSkillRead])
def list_employee_skills(
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db.query(models.EmployeeSkill).filter(models.EmployeeSkill.employee_id == employee_id).all()


@router.post("/{employee_id}/skills", response_model=schemas.EmployeeSkillRead, status_code=status.HTTP_201_CREATED)
def add_employee_skill(
    employee_id: int,
    skill_in: schemas.EmployeeSkillCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill_name = skill_in.skill.strip()
    if not skill_name:
        raise HTTPException(status_code=400, detail="Skill cannot be empty")

    existing = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.employee_id == employee_id,
        models.EmployeeSkill.skill == skill_name,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    new_skill = models.EmployeeSkill(employee_id=employee_id, skill=skill_name)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@router.delete("/{employee_id}/skills/{skill_name}")
def remove_employee_skill(
    employee_id: int,
    skill_name: str,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.employee_id == employee_id,
        models.EmployeeSkill.skill == skill_name,
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found for this employee")

    db.delete(skill)
    db.commit()
    return {"message": "Skill removed"}


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.delete(employee)
    db.commit()