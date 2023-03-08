from dotenv import load_dotenv
from fastapi_login import LoginManager
from database import DBContext
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import os
import crud



load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"

class NotAuthenticatedException(Exception):
    pass


def not_authenticated_exception_handler(request, exception):
    return RedirectResponse("/login")


manager.not_authenticated_exception = NotAuthenticatedException

@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        # if db does not exist create it
        with DBContext() as db:
            return crud.get_user_by_username(db=db, username=username)
    return crud.get_user_by_username(db=db, username=username)

def get_db():
    with DBContext() as db:
        yield db

