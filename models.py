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
        orm_mode = True
        
