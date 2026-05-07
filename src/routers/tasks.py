# src/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.database import SessionLocal
from src import models, schemas
from src.security.roles import require_roles
from src.security.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = db.query(models.Project).filter(models.Project.id == task_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Admins can create tasks in any project
    # Employees must be a member of the project
    if current_user.role != "admin":
        member = db.query(models.ProjectMember).filter(
            models.ProjectMember.project_id == task_in.project_id,
            models.ProjectMember.employee_id == current_user.id,
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this project",
            )

    if task_in.sprint_id is not None:
        sprint = db.query(models.Sprint).filter(models.Sprint.id == task_in.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")

    if task_in.components_id is not None:
        component = db.query(models.Component).filter(models.Component.id == task_in.components_id).first()
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
    components_id: int | None = None,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    q = db.query(models.Task)

    if project_id is not None:
        q = q.filter(models.Task.project_id == project_id)
    if sprint_id is not None:
        q = q.filter(models.Task.sprint_id == sprint_id)
    if components_id is not None:
        q = q.filter(models.Task.components_id == components_id)
    if status is not None:
        q = q.filter(models.Task.status == status)
    if priority is not None:
        q = q.filter(models.Task.priority == priority)
    if search:
        term = f"%{search.strip()}%"
        q = q.filter(
            or_(
                models.Task.title.ilike(term),
                models.Task.status.ilike(term),
                models.Task.priority.ilike(term),
            )
        )

    return q.all()


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.TaskRead)
@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Admins can update any task
    # Employees can only update tasks in projects they are a member of
    if current_user.role != "admin":
        member = db.query(models.ProjectMember).filter(
            models.ProjectMember.project_id == task.project_id,
            models.ProjectMember.employee_id == current_user.id,
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this project",
            )

    data = task_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()


# ── Task Assignments ──────────────────────────────────────────────────────────

@router.get("/{task_id}/assignments", response_model=list[schemas.TaskAssignmentRead])
def list_task_assignments(
    task_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    assignments = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id == task_id
    ).all()

    result = []
    for a in assignments:
        employee = db.query(models.Employee).filter(
            models.Employee.id == a.employee_id
        ).first()
        result.append({
            "id": a.id,
            "task_id": a.task_id,
            "employee_id": a.employee_id,
            "assigned_at": a.assigned_at,
            "full_name": employee.full_name if employee else "Unknown",
        })

    return result


@router.post("/{task_id}/assignments", response_model=schemas.TaskAssignmentRead, status_code=status.HTTP_201_CREATED)
def assign_employee(
    task_id: int,
    assignment_in: schemas.TaskAssignmentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    employee = db.query(models.Employee).filter(models.Employee.id == assignment_in.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id == task_id,
        models.TaskAssignment.employee_id == assignment_in.employee_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee already assigned to this task")

    assignment = models.TaskAssignment(task_id=task_id, employee_id=assignment_in.employee_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{task_id}/assignments/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign_employee(
    task_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    assignment = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id == task_id,
        models.TaskAssignment.employee_id == employee_id,
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()


# ── Task Labels ───────────────────────────────────────────────────────────────

@router.get("/{task_id}/labels", response_model=list[schemas.TaskLabelRead])
def list_task_labels(
    task_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db.query(models.TaskLabel).filter(models.TaskLabel.task_id == task_id).all()


@router.post("/{task_id}/labels", response_model=schemas.TaskLabelRead, status_code=status.HTTP_201_CREATED)
def add_task_label(
    task_id: int,
    label_in: schemas.TaskLabelCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    label = db.query(models.Label).filter(models.Label.id == label_in.label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    existing = db.query(models.TaskLabel).filter(
        models.TaskLabel.task_id == task_id,
        models.TaskLabel.label_id == label_in.label_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Label already added to this task")

    task_label = models.TaskLabel(task_id=task_id, label_id=label_in.label_id)
    db.add(task_label)
    db.commit()
    db.refresh(task_label)
    return task_label

# ── Task Comments ─────────────────────────────────────────────────────────────

@router.get("/{task_id}/comments", response_model=list[schemas.CommentRead])
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

@router.post("/{task_id}/comments", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
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


@router.delete("/{task_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task_label(
    task_id: int,
    label_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "employee")),
):
    task_label = db.query(models.TaskLabel).filter(
        models.TaskLabel.task_id == task_id,
        models.TaskLabel.label_id == label_id,
    ).first()
    if not task_label:
        raise HTTPException(status_code=404, detail="Label not found on this task")
    db.delete(task_label)
    db.commit()