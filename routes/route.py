from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates

route = APIRouter()
templates = Jinja2Templates(directory="templates")

@route.get("/")
def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'title': "Home"})