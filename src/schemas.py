from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str

class EmployeeCreate(EmployeeBase):
    password: str  # password will come from the user

class EmployeeUpdate(EmployeeBase):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None

class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# New schema for the login endpoint
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmployeeSkillCreate(BaseModel):
    skill: str

class EmployeeSkillRead(BaseModel):
    id: int
    employee_id: int
    skill: str

    class Config:
        from_attributes = True
