# main.py
import bcrypt
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from src.routers import tasks, employees, sprints
from src.security.passwords import verify_password, hash_password
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeeHive TTM API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tasks.router)
app.include_router(employees.router)
app.include_router(sprints.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "TTM API is running"}


@app.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.put("/projects/{project_id}", response_model=schemas.ProjectRead)
@app.patch("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    if project.start_date and project.end_date and project.end_date < project.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date cannot be before start_date",
        )

    db.commit()
    db.refresh(project)
    return project


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
        "role": employee.role,
    }

#employee skills endpoint
@app.get("/employees/{employee_id}/skills", response_model=list[schemas.EmployeeSkillRead])
def list_employee_skills(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    skills = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.employee_id == employee_id
    ).all()

    return skills


@app.post("/employees/{employee_id}/skills", response_model=schemas.EmployeeSkillRead, status_code=status.HTTP_201_CREATED)
def add_employee_skill(employee_id: int, skill_in: schemas.EmployeeSkillCreate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill_name = skill_in.skill.strip()
    if not skill_name:
        raise HTTPException(status_code=400, detail="Skill cannot be empty")

    existing = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.employee_id == employee_id,
        models.EmployeeSkill.skill == skill_name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    new_skill = models.EmployeeSkill(
        employee_id=employee_id,
        skill=skill_name
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@app.delete("/employees/{employee_id}/skills/{skill_name}")
def remove_employee_skill(employee_id: int, skill_name: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.employee_id == employee_id,
        models.EmployeeSkill.skill == skill_name
    ).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found for this employee")

    db.delete(skill)
    db.commit()

    return {"message": "Skill removed"}
