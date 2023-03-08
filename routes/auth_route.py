from fastapi import Request, Response, Depends, status, Form, APIRouter
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from services import manager, get_db

from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from passlib.context import CryptContext

import crud
import schemas

route = APIRouter()
templates = Jinja2Templates(directory="templates")
ACCESS_TOKEN_EXPIRE_TIME = 60

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(unhashed_password, hashed_password):
    return password_context.verify(unhashed_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        print('user does not exist')
        return None
    if not verify_password(unhashed_password=password, hashed_password=user.hashed_password):
        print('invalid password')
        return None
    return user

def get_hashed_password(unhashed_password):
    return password_context.hash(unhashed_password)

@route.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'title': "Login"})


@route.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username,
                             password=form_data.password, db=db)
    if not user:
        return templates.TemplateResponse(
            'login.html', 
            {'request': request, 'title': "Login", "invalid": True}, 
            status_code=status.HTTP_401_UNAUTHORIZED
            )
    access_token_expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    access_token = manager.create_access_token(
        data={"sub": user.username},
        expires=access_token_expires_time
    )
    response = RedirectResponse("/tasks", status_code=status.HTTP_200_OK)
    manager.set_cookie(response=response, token=access_token)
    return response


@route.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register"})


@route.post("/register")
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
            "/login", status_code=status.HTTP_201_CREATED)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "title": "Register", "invalid": True},
                                          status_code=status.HTTP_400_BAD_REQUEST)


@route.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/")
    manager.set_cookie(response=response, token=None)
    return response