import os
from dotenv import load_dotenv
from fastapi_login import LoginManager



load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"