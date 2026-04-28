# src/models.py
from sqlalchemy import BigInteger, Column, String, Boolean, TIMESTAMP, text, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    hashed_password = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    comments = relationship("Comment", back_populates="employee")
    skills = relationship("EmployeeSkill", back_populates="employee")
    assignments = relationship("TaskAssignment", back_populates="employee")
    project_memberships = relationship("ProjectMember", back_populates="employee")


class EmployeeSkill(Base):
    __tablename__ = "employee_skills"

    id = Column(BigInteger, primary_key=True, index=True)
    employee_id = Column(BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    skill = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    employee = relationship("Employee", back_populates="skills")


class Project(Base):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(Text, nullable=True, default="Active")

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    sprints = relationship("Sprint", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    components = relationship("Component", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    labels = relationship("Label", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    member_role = Column(Text, nullable=True)
    joined_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    project = relationship("Project", back_populates="members")
    employee = relationship("Employee", back_populates="project_memberships")


class Component(Base):
    __tablename__ = "components"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)

    project = relationship("Project", back_populates="components")
    tasks = relationship("Task", back_populates="component")


class Label(Base):
    __tablename__ = "labels"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)

    project = relationship("Project", back_populates="labels")
    task_labels = relationship("TaskLabel", back_populates="label", cascade="all, delete-orphan", passive_deletes=True)


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    project = relationship("Project", back_populates="sprints")
    tasks = relationship("Task", back_populates="sprint", passive_deletes=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    sprint_id = Column(BigInteger, ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True)
    components_id = Column(BigInteger, ForeignKey("components.id", ondelete="SET NULL"), nullable=True)
    title = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="To-Do")
    priority = Column(Text, nullable=False, default="Medium")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False, onupdate=text("NOW()"))
    description = Column(Text, nullable=True)

    project = relationship("Project", back_populates="tasks")
    sprint = relationship("Sprint", back_populates="tasks")
    component = relationship("Component", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan", passive_deletes=True)
    assignments = relationship("TaskAssignment", back_populates="task", cascade="all, delete-orphan", passive_deletes=True)
    task_labels = relationship("TaskLabel", back_populates="task", cascade="all, delete-orphan", passive_deletes=True)


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    task = relationship("Task", back_populates="assignments")
    employee = relationship("Employee", back_populates="assignments")


class TaskLabel(Base):
    __tablename__ = "task_labels"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    label_id = Column(BigInteger, ForeignKey("labels.id", ondelete="CASCADE"), nullable=False)

    task = relationship("Task", back_populates="task_labels")
    label = relationship("Label", back_populates="task_labels")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    task = relationship("Task", back_populates="comments")
    employee = relationship("Employee", back_populates="comments")


class Template(Base):
    __tablename__ = "templates"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    role = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)