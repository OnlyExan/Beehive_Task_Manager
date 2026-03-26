from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models, schemas

router = APIRouter(prefix="/sprints", tags=["sprints"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.SprintRead, status_code=status.HTTP_201_CREATED)
def create_sprint(sprint_in: schemas.SprintCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == sprint_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    sprint = models.Sprint(**sprint_in.model_dump())
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint

@router.get("", response_model=list[schemas.SprintRead])
def list_sprints(project_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Sprint)
    if project_id is not None:
        q = q.filter(models.Sprint.project_id == project_id)
    return q.all()

@router.get("/{sprint_id}", response_model=schemas.SprintRead)
def get_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.put("/{sprint_id}", response_model=schemas.SprintRead)
@router.patch("/{sprint_id}", response_model=schemas.SprintRead)
def update_sprint(sprint_id: int, sprint_in: schemas.SprintUpdate, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    data = sprint_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(sprint, field, value)

    if sprint.start_date and sprint.end_date and sprint.end_date < sprint.start_date:
        raise HTTPException(status_code=400, detail="end_date cannot be before start_date")

    db.commit()
    db.refresh(sprint)
    return sprint