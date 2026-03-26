from datetime import date

from pydantic import BaseModel, EmailStr, field_validator, model_validator


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


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value

    @model_validator(mode="after")
    def validate_project_update(self):
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("name cannot be null")

        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class ProjectRead(ProjectBase):
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


# ----- Component -----
class ComponentBase(BaseModel):
    project_id: int
    name: str

class ComponentCreate(ComponentBase):
    pass

class ComponentRead(ComponentBase):
    id: int

    class Config:
        from_attributes = True

# ----- Task -----
class TaskBase(BaseModel):
    project_id: int
    sprint_id: int | None = None
    title: str
    status: str = "To-Do"      # To-Do, In-Progress, Review, Done
    priority: str = "Medium"   # Low, Medium, High

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    sprint_id: int | None = None
    title: str | None = None
    status: str | None = None
    priority: str | None = None

class TaskRead(TaskBase):
    id: int

    class Config:
        from_attributes = True

# ----- Sprint -----
class SprintBase(BaseModel):
    project_id: int
    name: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self

class SprintCreate(SprintBase):
    pass

class SprintUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self

class SprintRead(SprintBase):
    id: int

    class Config:
        from_attributes = True