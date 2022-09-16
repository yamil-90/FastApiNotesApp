from datetime import timedelta
from fastapi import FastAPI, Request, Response, Depends, status, Form, Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from database import SessionLocal, engine, DBContext
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from routes.tasks_route import route as task_route
from services import manager


import models
import crud
import schemas




password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_TIME = 60
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# TODO should be in import
def get_db():
    with DBContext() as db:
        yield db


def get_hashed_password(unhashed_password):
    return password_context.hash(unhashed_password)


def verify_password(unhashed_password, hashed_password):
    return password_context.verify(unhashed_password, hashed_password)


@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        # if db does not exist create it
        with DBContext() as db:
            return crud.get_user_by_username(db=db, username=username)
    return crud.get_user_by_username(db=db, username=username)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        print('user does not exist')
        return None
    if not verify_password(unhashed_password=password, hashed_password=user.hashed_password):
        print('invalid password')
        return None
    return user


class NotAuthenticatedException(Exception):
    pass


def not_authenticated_exception_handler(request, exception):
    return RedirectResponse("/login")


manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException,
                          not_authenticated_exception_handler)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'title': "Home"})

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'title': "Login"})


@app.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username,
                             password=form_data.password, db=db)
    if not user:
        return templates.TemplateResponse('login.html', {'request': request, 'title': "Login", "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    access_token = manager.create_access_token(
        data={"sub": user.username},
        expires=access_token_expires_time
    )
    response = RedirectResponse("/tasks", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response=response, token=access_token)
    return response


@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register"})


@app.post("/register")
def post_register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    hashed_password = get_hashed_password(password)
    invalid = False
    if crud.get_user_by_username(db=db, username=username):
        invalid = True
    if crud.get_user_by_email(db=db, email=email):
        invalid = True
    if not invalid:
        crud.create_user(db=db, user=schemas.UserCreate(
            username=username, email=email, name=name, hashed_password=hashed_password))
        response = RedirectResponse(
            "/login", status_code=status.HTTP_302_FOUND)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "title": "Register", "invalid": True},
                                          status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/")
    manager.set_cookie(response=response, token=None)
    return response

app.include_router(task_route)

# print(get_hashed_password('pass'))
