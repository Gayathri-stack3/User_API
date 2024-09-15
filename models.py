from typing import Union, List
from pydantic import BaseModel

# Define your UserModel
class UserModel(BaseModel):
    first_name: str
    last_name: str
    age: float
    is_active: bool
    gender: str  # or List[str] depending on your use case
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the User model (table structure)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Float)
    is_active = Column(Boolean, default=True)
    gender = Column(String)

    class Config:
        orm_mode = True

# SuccessResponse Model
class SuccessResponse(BaseModel):
    status: str
    data: Union[UserModel, List[UserModel], dict]

    class Config:
        orm_mode = True
