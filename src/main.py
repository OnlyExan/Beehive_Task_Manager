# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeeHive TTM API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "TTM API is running"}


@app.post("/employees", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee_in: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    employee = models.Employee(
        full_name=employee_in.full_name, 
        email=employee_in.email,
        role=employee_in.role,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(employee_id: int, employee_in: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
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

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employees", response_model=list[schemas.EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    return employees

@app.get("/employees/debug")
def debug_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()
