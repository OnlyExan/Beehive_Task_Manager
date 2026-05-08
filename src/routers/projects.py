# src/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models, schemas
from src.security.roles import require_roles

router = APIRouter(prefix="/projects", tags=["projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[schemas.ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    return db.query(models.Project).all()


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = models.Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=schemas.ProjectRead)
@router.patch("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_in: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    if project.start_date and project.end_date and project.end_date < project.start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date cannot be before start_date")

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


# ── Project Members ───────────────────────────────────────────────────────────

@router.get("/{project_id}/members", response_model=list[schemas.ProjectMemberRead])
def list_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id
    ).all()

    # Enrich with employee full_name
    result = []
    for member in members:
        employee = db.query(models.Employee).filter(
            models.Employee.id == member.employee_id
        ).first()
        result.append({
            "id": member.id,
            "project_id": member.project_id,
            "employee_id": member.employee_id,
            "member_role": member.member_role,
            "joined_at": member.joined_at,
            "full_name": employee.full_name if employee else "Unknown",
        })

    return result


@router.post("/{project_id}/members", response_model=schemas.ProjectMemberRead, status_code=status.HTTP_201_CREATED)
def add_project_member(
    project_id: int,
    member_in: schemas.ProjectMemberCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    employee = db.query(models.Employee).filter(models.Employee.id == member_in.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.employee_id == member_in.employee_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee is already a member of this project")

    member = models.ProjectMember(
        project_id=project_id,
        employee_id=member_in.employee_id,
        member_role=member_in.member_role,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{project_id}/members/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project_member(
    project_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    member = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.employee_id == employee_id,
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found on this project")
    db.delete(member)
    db.commit()


# ── Components ────────────────────────────────────────────────────────────────

@router.get("/{project_id}/components", response_model=list[schemas.ComponentRead])
def list_components(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    return db.query(models.Component).filter(models.Component.project_id == project_id).all()


@router.post("/{project_id}/components", response_model=schemas.ComponentRead, status_code=status.HTTP_201_CREATED)
def create_component(
    project_id: int,
    component_in: schemas.ComponentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    component = models.Component(project_id=project_id, name=component_in.name)
    db.add(component)
    db.commit()
    db.refresh(component)
    return component


@router.delete("/{project_id}/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(
    project_id: int,
    component_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    component = db.query(models.Component).filter(
        models.Component.id == component_id,
        models.Component.project_id == project_id,
    ).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    db.delete(component)
    db.commit()


# ── Labels ────────────────────────────────────────────────────────────────────

@router.get("/{project_id}/labels", response_model=list[schemas.LabelRead])
def list_labels(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    return db.query(models.Label).filter(models.Label.project_id == project_id).all()


@router.post("/{project_id}/labels", response_model=schemas.LabelRead, status_code=status.HTTP_201_CREATED)
def create_label(
    project_id: int,
    label_in: schemas.LabelCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    label = models.Label(project_id=project_id, name=label_in.name)
    db.add(label)
    db.commit()
    db.refresh(label)
    return label


@router.delete("/{project_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(
    project_id: int,
    label_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    label = db.query(models.Label).filter(
        models.Label.id == label_id,
        models.Label.project_id == project_id,
    ).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(label)
    db.commit()