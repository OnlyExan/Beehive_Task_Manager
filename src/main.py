# src/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from src.routers import tasks, employees, sprints, auth, setup, projects
from src.security.roles import require_roles
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeeHive TTM API")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers — setup first since it requires no auth
app.include_router(setup.router)
app.include_router(auth.router)
app.include_router(projects.router)
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


# ── Employee Skills ───────────────────────────────────────────────────────────

@app.get("/employees/{employee_id}/skills", response_model=list[schemas.EmployeeSkillRead])
def list_employee_skills(
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db.query(models.EmployeeSkill).filter(models.EmployeeSkill.employee_id == employee_id).all()


@app.post("/employees/{employee_id}/skills", response_model=schemas.EmployeeSkillRead, status_code=status.HTTP_201_CREATED)
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


@app.delete("/employees/{employee_id}/skills/{skill_name}")
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


# ── Task Comments ─────────────────────────────────────────────────────────────

@app.get("/tasks/{task_id}/comments", response_model=list[schemas.CommentRead])
def list_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.task_id == task_id)
        .order_by(models.Comment.created_at.asc())
        .all()
    )

    # Enrich each comment with the employee name
    result = []
    for comment in comments:
        employee = db.query(models.Employee).filter(
            models.Employee.id == comment.employee_id
        ).first()
        comment_dict = {
            "id": comment.id,
            "task_id": comment.task_id,
            "employee_id": comment.employee_id,
            "comment_text": comment.comment_text,
            "created_at": comment.created_at,
            "employee_name": employee.full_name if employee else "Unknown",
        }
        result.append(comment_dict)

    return result

@app.post("/tasks/{task_id}/comments", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
def add_task_comment(
    task_id: int,
    comment_in: schemas.CommentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    employee = db.query(models.Employee).filter(models.Employee.id == comment_in.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_comment = models.Comment(
        task_id=task_id,
        employee_id=comment_in.employee_id,
        comment_text=comment_in.comment_text,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}