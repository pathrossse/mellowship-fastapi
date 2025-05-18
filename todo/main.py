from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, auth
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from .routers import user

app = FastAPI()

app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_todo = models.Todo(
        description=request.description,
        deadline=request.deadline,
        done=request.done,
        user_id=current_user.id 
       
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

@app.get("/todo")
def get_all(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos

@app.get("/todo/groups", status_code=status.HTTP_200_OK)
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

@app.get("/todo/{id}", status_code=200)
def get_todo(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id  
    ).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")
    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    result = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id  
    ).delete(synchronize_session=False)
    
    if result == 0:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    db.commit()
    return f"Todo with {id} deleted successfully!"

@app.put("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id, request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo_query = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id 
    )
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    update_data = {
        "description": request.description,
        "deadline": request.deadline,
        "done": request.done
    }
    
    todo_query.update(update_data, synchronize_session=False)
    db.commit()
    
    return {"message": f"Todo with id {id} updated successfully"}

@app.put("/todo/{id}/mark-done", status_code=status.HTTP_202_ACCEPTED)
def mark_done(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo_query = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id 
    )
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    todo.done = True
    db.commit()
    
    return {"message": f"Todo with ID: {id} marked as done"}

