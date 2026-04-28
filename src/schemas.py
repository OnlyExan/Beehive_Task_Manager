# src/schemas.py
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str


class EmployeeCreate(EmployeeBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")
        if not any(c.isalpha() for c in value):
            raise ValueError("Password must contain at least one letter")
        return value


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


# ── Employee Skill ────────────────────────────────────────────────────────────

class EmployeeSkillCreate(BaseModel):
    skill: str


class EmployeeSkillRead(BaseModel):
    id: int
    employee_id: int
    skill: str

    class Config:
        from_attributes = True


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Project ───────────────────────────────────────────────────────────────────

class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = "Active"

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
    status: str | None = None

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


# ── Project Member ────────────────────────────────────────────────────────────

class ProjectMemberCreate(BaseModel):
    employee_id: int
    member_role: str | None = None


class ProjectMemberRead(BaseModel):
    id: int
    project_id: int
    employee_id: int
    member_role: str | None = None
    joined_at: datetime
    full_name: str | None = None  # add this

    class Config:
        from_attributes = True


# ── Component ─────────────────────────────────────────────────────────────────

class ComponentBase(BaseModel):
    project_id: int
    name: str


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: str | None = None


class ComponentRead(ComponentBase):
    id: int

    class Config:
        from_attributes = True


# ── Label ─────────────────────────────────────────────────────────────────────

class LabelBase(BaseModel):
    project_id: int
    name: str


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: str | None = None


class LabelRead(LabelBase):
    id: int

    class Config:
        from_attributes = True


# ── Sprint ────────────────────────────────────────────────────────────────────

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


# ── Task ──────────────────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    project_id: int
    sprint_id: int | None = None
    components_id: int | None = None
    title: str
    status: str = "To-Do"
    priority: str = "Medium"
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    sprint_id: int | None = None
    components_id: int | None = None
    title: str | None = None
    status: str | None = None
    priority: str | None = None
    description: str | None = None

class TaskRead(TaskBase):
    id: int

    class Config:
        from_attributes = True


# ── Task Assignment ───────────────────────────────────────────────────────────

class TaskAssignmentCreate(BaseModel):
    employee_id: int


class TaskAssignmentRead(BaseModel):
    id: int
    task_id: int
    employee_id: int
    assigned_at: datetime
    full_name: str | None = None  # add this

    class Config:
        from_attributes = True


# ── Task Label ────────────────────────────────────────────────────────────────

class TaskLabelCreate(BaseModel):
    label_id: int


class TaskLabelRead(BaseModel):
    id: int
    task_id: int
    label_id: int
    label: LabelRead | None = None

    class Config:
        from_attributes = True


# ── Comment ───────────────────────────────────────────────────────────────────

class CommentBase(BaseModel):
    employee_id: int
    comment_text: str

    @field_validator("comment_text")
    @classmethod
    def validate_comment(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("comment cannot be empty")
        return value


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    comment_text: str

    @field_validator("comment_text")
    @classmethod
    def validate_comment(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("comment cannot be empty")
        return value


class CommentRead(CommentBase):
    id: int
    task_id: int
    created_at: datetime
    employee_name: str | None = None

    class Config:
        from_attributes = True