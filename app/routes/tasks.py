from sqlalchemy import select
from fastapi import APIRouter, Depends
from config.database import get_db
from app.schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from app.models.tasks import Task

task_router = APIRouter(tags=["tasks"])

# Create a task
@task_router.post('/tasks/create')
def create_task(request: TaskCreateSchema, session=Depends(get_db)):
    new_task = Task(title=request.title, description=request.description, is_completed=request.is_completed)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

# Read a task
@task_router.get('/tasks/read/{task_id}')
def read_task(task_id: int, session=Depends(get_db)):
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    return task 

# Update a task
@task_router.put('/tasks/update/{task_id}')
def update_task(task_id: int, request: TaskUpdateSchema, session=Depends(get_db)):
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    task.title = request.title
    task.description = request.description
    task.is_completed = request.is_completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Delete a task
@task_router.delete('/tasks/delete/{task_id}')
def delete_task(task_id: int, session=Depends(get_db)):
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}

# Get all tasks
@task_router.get('/tasks/all')
def list_tasks(session=Depends(get_db)):
    tasks = session.execute(select(Task)).scalars().all()
    return tasks