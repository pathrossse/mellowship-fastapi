from fastapi import FastAPI, Depends, status, Response, HTTPException
from .. import schemas, auth
from ..db.database import get_db
from sqlmodel import Session, select
from datetime import datetime
from ..db import models

router = APIRouter(
    prefix="/todo",
    tags=["todos"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_todo = models.Todo(
        description=request.description,
        deadline=request.deadline,
        done=request.done,
        user_id=current_user.id 
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

@router.get("")
def get_all(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos

@router.get("/groups", status_code=status.HTTP_200_OK)
def group_todos(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()

    current_time = datetime.now()
    
    completed = []
    to_be_done = []
    time_elapsed = []

    for todo in todos:
        if todo.done:
            completed.append(todo)
        elif todo.deadline < current_time:
            time_elapsed.append(todo)
        else:
            to_be_done.append(todo)
    
    return {
        "completed": completed,
        "to_be_done": to_be_done,
        "time_elapsed": time_elapsed
    }

@router.get("/{id}", status_code=200)
def get_todo(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
  statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id, request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
      
    todo.description = request.description
    todo.deadline = request.deadline
    todo.done = request.done
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return {"message": f"Todo with id {id} updated successfully"}

@router.put("/{id}/mark-done", status_code=status.HTTP_202_ACCEPTED)
def mark_done(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    todo.done = True
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return {"message": f"Todo with ID: {id} marked as done"}
