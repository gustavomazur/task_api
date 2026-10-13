
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(**task.model_dump())
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    task = db.query(models.Task).all()
    return task

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task com esse id : {id} não existe ")

    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):

    task_query = db.query(models.Task).filter(models.Task.id == id)

    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'task com esse id: {id} não existe')

    task_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.TaskAtulizacao)
def update_task(id: int, update_task: schemas.TaskAtulizacao, db: Session = Depends(get_db)):

    task_query = db.query(models.Task).filter(models.Task.id == id)

    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'task com esse id: {id} não existe')

    task_query.update(update_task.model_dump(exclude_unset=True),
                    synchronize_session=False)

    db.commit()

    return task_query.first()


    