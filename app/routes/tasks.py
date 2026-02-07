from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from app.schemas.tasks import *
from app.models.tasks import TaskModel
from sqlalchemy.orm import Session
from config.database import get_db, SessionLocal
from typing import List
from sqlalchemy import func

task_router = APIRouter(tags=["tasks"])



@task_router.get("/all", response_model=List[TaskResponseSchema])
def retrieve_tasks_list(
    db: Session = Depends(get_db),
    completed: bool = Query(None, description='Filter tasks based on being completed or not'),
    offset: int = Query(0, ge=0, description='Use for paginating based on passed items'),
    limit: int = Query(5, ge=0, le=50, description='Limiting the number of items to retrieve'),
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

    response = query.limit(limit).offset(offset).all()
    return response


@task_router.get("/{task_id}",response_model=TaskResponseSchema)
def retrieve_task_detail(task_id: int = Path(..., gt=0),db:Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404,detail="Task not found")
    return task_obj


@task_router.post("/create" ,response_model=TaskResponseSchema)
def create_task(request:TaskCreateSchema,db:Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@task_router.put("/edit/{task_id}", response_model=TaskResponseSchema)
def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
    db.commit() 
    db.refresh(task_obj)  
    return task_obj 



def get_id_range():
    session = SessionLocal()
    try:
        min_id, max_id = session.query(
            func.min(TaskModel.id),
            func.max(TaskModel.id)
        ).one()
        return min_id, max_id
    finally:
        session.close()

min_id, max_id = get_id_range()
        
@task_router.delete("/delete", status_code=204)
def delete_tasks(
    task_id: Optional[int] = Query(None, ge=1),
    from_id: Optional[int] = Query(None, ge=1, example=f'min available id: {min_id}'),
    to_id: Optional[int] = Query(None, ge=1,  example=f'max available id: {max_id}'),
    delete_all: bool = Query(False),
    db: Session = Depends(get_db)
):
    q = db.query(TaskModel)

    if delete_all:
        q.delete(synchronize_session=False)

    elif task_id is not None:
        if not q.filter(TaskModel.id == task_id).first():
            raise HTTPException(404, "Task not found")
        q.filter(TaskModel.id == task_id).delete(synchronize_session=False)

    elif from_id is not None and to_id is not None:
        if to_id < from_id:
            raise HTTPException(400, "Invalid range")
        q.filter(TaskModel.id.between(from_id, to_id)).delete(synchronize_session=False)

    else:
        raise HTTPException(
            400,
            "Provide task_id or from_id & to_id or set delete_all=true"
        )

    db.commit()
