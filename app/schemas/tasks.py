from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBaseSchema(BaseModel):
    id: Optional[int] = None

class TaskCreateSchema(TaskBaseSchema):
    title: str = Field(..., min_length=1)
    description: str = ""
    is_done: bool = False

    class Config:
        orm_mode = True

class TaskReadSchema(TaskBaseSchema):
    title: str
    description: str
    is_done: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TaskUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_done: Optional[bool]

    class Config:
        orm_mode = True
