from pydantic import BaseModel
from typing import Optional

class TaskBaseSchema(BaseModel):
    id: Optional[int] = None
    
    
class TaskCreateSchema(TaskBaseSchema):
    title: str
    description: str = ""
    is_done: bool = False

    class Config:
        orm_mode = True 