from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(String, unique=True, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, unique=False, nullable=True)
    hashed_password = Column(String, unique=False, nullable=False, index=False)

    items = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "task"

    id = Column(String, unique=True, primary_key=True, index=True, nullable=False)
    text =  Column(String,index=True, nullable=False)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="items")