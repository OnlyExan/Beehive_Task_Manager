# routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.database import SessionLocal
from sqlalchemy.orm import Session
from src import models, schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    # optional: validate foreign keys exist
    project = db.query(models.Project).filter(models.Project.id == task_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if task_in.sprint_id is not None:
        sprint = db.query(models.Sprint).filter(models.Sprint.id == task_in.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")

    if task_in.component_id is not None:
        component = db.query(models.Component).filter(models.Component.id == task_in.component_id).first()
        if not component:
            raise HTTPException(status_code=404, detail="Component not found")

    task = models.Task(**task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(
    project_id: int | None = None,
    sprint_id: int | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Task)
    if project_id is not None:
        q = q.filter(models.Task.project_id == project_id)
    if sprint_id is not None:
        q = q.filter(models.Task.sprint_id == sprint_id)
    return q.all()

@router.put("/{task_id}", response_model=schemas.TaskRead)
@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = task_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

