from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import DateTime

class TaskBaseSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = False


class TaskCreateSchema(TaskBaseSchema):
    class Config:
        orm_mode = True


class TaskUpdateSchema(BaseModel):
    class Config:
        orm_mode = True


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description='Unique identifier of the object')