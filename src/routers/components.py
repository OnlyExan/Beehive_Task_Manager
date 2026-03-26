from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models, schemas


router = APIRouter(prefix="/components", tags=["components"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.ComponentRead, status_code=status.HTTP_201_CREATED)
def create_component(component_in: schemas.ComponentCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == component_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    component = models.Component(**component_in.model_dump())
    db.add(component)
    db.commit()
    db.refresh(component)
    return component

@router.get("", response_model=list[schemas.ComponentRead])
def list_components(project_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Component)
    if project_id is not None:
        q = q.filter(models.Component.project_id == project_id)
    return q.all()