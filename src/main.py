# main.py
import bcrypt
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from src.security.passwords import verify_password, hash_password

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
        hashed_password=hash_password(employee_in.password)  # scramble before saving
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

# NEW: Login endpoint
@app.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.email == credentials.email).first()

    if not employee or not verify_password(credentials.password, employee.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "id": employee.id,
        "full_name": employee.full_name,
        "email": employee.email,
        "role": employee.role
    }
