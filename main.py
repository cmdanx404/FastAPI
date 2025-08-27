from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Todo
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic schemas
class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# Read (with pagination option)
@app.get("/todos/", response_model=list[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Todo).offset(skip).limit(limit).all()


# Update (title and/or completed)
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    db.commit()
    db.refresh(todo)
    return todo


# Delete
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Deleted"}
