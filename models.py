from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

# Database table
class ProductDB(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    qty = Column(Integer)

# API schema
class Product(BaseModel):
    id: int
    name: str
    qty: int

    class Config:
        from_attributes = True

from sqlalchemy import Boolean

# User table
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

# User schema
class User(BaseModel):
    username: str
    password: str