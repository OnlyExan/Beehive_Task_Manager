# models.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from .database import Base

# Below is a template of a SQLAlchemy model. You can replace it with your actual models as needed.
class employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("TRUE"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
