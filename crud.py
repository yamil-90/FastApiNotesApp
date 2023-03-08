from sqlalchemy.orm import Session
from models import User, Task
from schemas import UserCreate, TaskCreate
import uuid


def get_user(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    id = uuid.uuid4()
    while get_user(db=db, id=str(id)):
        id = uuid.uuid4()
    db_user = User(id=str(id),username=user.username,name=user.name,email=user.email,hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks_by_user_id(db: Session, id: str, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.user_id == id).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, id: str):
    return db.query(Task).filter(Task.id == id).first()

def add_taks(db: Session, task: TaskCreate, id: str):
    if not get_user(db=db, id=str(id)):
        return None
    task_id = uuid.uuid4()
    while get_task_by_id(db=db, id=str(id)):
        task_id = uuid.uuid4()
    db_task = Task(id=str(task_id),text=task.text, user_id=id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_tasks(db: Session, id: str):
    db.query(Task).filter(Task.id == id).delete()
    db.commit()

    # pytest para crear cosas random
