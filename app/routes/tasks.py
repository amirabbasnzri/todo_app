from fastapi import APIRouter, Path,Depends,HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import func
from app.schemas.tasks import *
from app.models.tasks import TaskModel
from sqlalchemy.orm import Session
from config.database import get_db
from typing import List
from datetime import datetime
from config.database import SessionLocal
from enum import Enum


task_router = APIRouter(tags=["tasks"])

def tasks_date_options():
    db: Session = SessionLocal()
    try:
        earliest = db.query(func.min(TaskModel.created_at)).scalar()
        latest = db.query(func.max(TaskModel.created_at)).scalar()
        return earliest, latest
    finally:
        db.close()

earliest, latest = tasks_date_options()


@task_router.get("/tasks/all", response_model=List[TaskResponseSchema])
def retrieve_tasks_list(
    db: Session = Depends(get_db),
    completed: bool = Query(None, description='Filter tasks based on being completed or not'),
    offset: int = Query(0, ge=0, description='Use for paginating based on passed items'),
    limit: int = Query(5, ge=0, le=50, description='Limiting the number of items to retrieve'),
    created_after: datetime = Query(None, ge=earliest, description=f'Earliest: {earliest}'),
    created_before: datetime = Query(None, le=latest, description=f'Latest {latest}')
):
    query = db.query(TaskModel)

    if completed is not None:
        response = query.filter(TaskModel.is_completed == completed).all()
        if not response:
            raise HTTPException(
                status_code=404,
                detail=f"There is no Task with status {completed}"
            )
        return response

    if created_after and created_before:
        response = query.filter(
            TaskModel.created_at > created_after,
            TaskModel.created_at < created_before
        ).all()

        if not response:
            raise HTTPException(
                status_code=404,
                detail="There are no tasks in this time period"
            )

        return response

    response = query.limit(limit).offset(offset).all()
    return response


@task_router.get("/tasks/{task_id}",response_model=TaskResponseSchema)
def retrieve_task_detail(task_id: int = Path(..., gt=0),db:Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404,detail="Task not found")
    return task_obj


@task_router.post("/tasks/create" ,response_model=TaskResponseSchema)
def create_task(request:TaskCreateSchema,db:Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@task_router.put("/tasks/edit/{task_id}", response_model=TaskResponseSchema)
def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
    db.commit() 
    db.refresh(task_obj)  
    return task_obj 


@task_router.delete("/tasks/delete/{task_id}",status_code=204)
def delete_task(task_id: int = Path(..., gt=0),db:Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()