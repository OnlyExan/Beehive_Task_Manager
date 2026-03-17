# models.py
from sqlalchemy import BigInteger, Column, Integer, String, Boolean, TIMESTAMP, text, Text
from src.database import Base

# Below is a template of a SQLAlchemy model. You can replace it with your actual models as needed.
class Employee(Base):
    __tablename__ = "employees"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )
    hashed_password = Column(Text, nullable=False) #new added line
