from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_status(db: Session, todo_id: int, todo_data: TodoUpdate):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return todo
