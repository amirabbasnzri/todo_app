from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBaseSchema(BaseModel):
    id: Optional[int] = None

class TaskCreateSchema(TaskBaseSchema):
    title: str = Field(..., min_length=1)
    description: str = ""
    is_completed: bool = False

    class Config:
        orm_mode = True


class TaskUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_completed: Optional[bool]

    class Config:
        orm_mode = True
