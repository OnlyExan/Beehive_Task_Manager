# src/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from src.routers import tasks, employees, sprints, auth, setup, projects
from src.security.roles import require_roles
from src.security.auth import get_current_user
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


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Admin can delete any comment, employee can only delete their own
    if current_user.role != "admin" and comment.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments",
        )

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}