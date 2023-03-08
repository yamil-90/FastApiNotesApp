from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.tasks_route import route as task_route
from routes.route import route as basic_route
from routes.auth_route import route as auth_route
from services import NotAuthenticatedException, not_authenticated_exception_handler, not_authenticated_exception_handler


templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_exception_handler(NotAuthenticatedException,
                          not_authenticated_exception_handler)


app.include_router(task_route)
app.include_router(basic_route)
app.include_router(auth_route)

