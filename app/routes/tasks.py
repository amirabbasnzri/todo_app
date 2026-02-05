from fastapi import APIRouter, Depends
from config.database import get_db
from app.schemas.tasks import TaskCreateSchema
from app.models.tasks import Task

task_router = APIRouter(tags=["tasks"])

@task_router.post('/tasks/create')
async def create_task(request: TaskCreateSchema, session=Depends(get_db)):
    new_task = Task(title=request.title, description=request.description, is_done=request.is_done)
    session.add(new_task)
    await session.flush()
    return new_task