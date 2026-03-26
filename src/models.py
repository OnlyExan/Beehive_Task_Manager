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

    ##tasks = relationship("Task", back_populates="project")
    ##sprints = relationship("Sprint", back_populates="project")
    ##components = relationship("Component", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)       # nullable
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True) # nullable

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

    ##project = relationship("Project", back_populates="tasks")
    ##sprint = relationship("Sprint", back_populates="tasks")
    ##component = relationship("Component", back_populates="tasks")

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(Text, nullable=False)

    ##project = relationship("Project", back_populates="components")
    ##tasks = relationship("Task", back_populates="component")