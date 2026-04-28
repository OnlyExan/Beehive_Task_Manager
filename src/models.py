# models.py
from sqlalchemy import BigInteger, Column, Integer, String, Boolean, TIMESTAMP, text, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    hashed_password = Column(Text, nullable=False)  # new added line
    role = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

class EmployeeSkill(Base):
    __tablename__ = "employee_skills"

    id = Column(BigInteger, primary_key=True, index=True)
    employee_id = Column(BigInteger, ForeignKey("employees.id"), nullable=False)
    skill = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

class Project(Base):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    ## relationship with tasks and sprints
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    sprints = relationship(
        "Sprint",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), nullable=False
    sprint_id = Column(Integer, ForeignKey("sprints.id"), ondelete="SET NULL", nullable=True), nullable=True       # nullable
    title = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="To-Do")
    priority = Column(Text, nullable=False, default="Medium")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
        onupdate=text("NOW()"),
    )

    project = relationship("Project", back_populates="tasks")
    sprint = relationship("Sprint", back_populates="tasks")
    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    project = relationship("Project", back_populates="sprints")

    name = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    project = relationship("Project", back_populates="sprints")

    tasks = relationship(
        "Task",
        back_populates="sprint",
        passive_deletes=True,
    )

class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

    task = relationship("Task", back_populates="comments")
    employee = relationship("Employee", back_populates="comments")