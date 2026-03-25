# models.py
from sqlalchemy import BigInteger, Column, Integer, String, Boolean, TIMESTAMP, text, Text, ForeignKey, Date
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
