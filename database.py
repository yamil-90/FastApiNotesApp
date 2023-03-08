from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


def db_name():
    # if os.getenv('RUN_ENV') == 'test':
    #         return 'test_' + os.getenv('DB_NAME')

    return os.getenv('DB_NAME')

db_name = str(db_name())

SQLALCHEMY_DATABASE_URI = "sqlite:///./todo_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class DBContext:
    def __init__(self) -> None:
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, et, ev, traceback):
        self.db.close()
