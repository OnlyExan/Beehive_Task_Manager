from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str

class EmployeeCreate(EmployeeBase):
    pass        # Will need to add password hash variable here when we add authentication

class EmployeeUpdate(EmployeeBase):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None

class EmployeeRead(EmployeeBase):
    id: int
    
    class Config: 
        from_attributes = True 