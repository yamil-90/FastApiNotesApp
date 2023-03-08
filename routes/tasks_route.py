from fastapi import Request, Depends, status, Form, Path, APIRouter
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from services import manager, get_db

import crud
import schemas

route = APIRouter()
templates = Jinja2Templates(directory="templates")

@route.get("/tasks")
def get_tasks(request: Request, db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    return templates.TemplateResponse("tasks.html", {"request": request,
                                                     "title": "Tasks",
                                                     "user": user,
                                                     "tasks": crud.get_tasks_by_user_id(db=db, id=user.id)})
@route.post("/tasks")
def add_task(request: Request, text: str = Form(...), db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    new_task = crud.add_taks(
        db=db, task=schemas.TaskCreate(text=text), id=user.id)
    if not new_task:
        return templates.TemplateResponse("tasks.html", {"request": request, 
        "title": "Task", 
        "user": user,
        "tasks": crud.get_tasks_by_user_id(db=db, id=str(user.id)), 
        "invalid": True}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return RedirectResponse("/tasks", status_code=status.HTTP_302_FOUND)

@route.get("/tasks/delete/{id}")
def delete_task(id: str = Path(...), db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    crud.delete_tasks(db=db, id=id)
    return RedirectResponse("/tasks")