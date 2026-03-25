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
