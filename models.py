from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from database import Base
from pydantic import BaseModel
from datetime import datetime

# Audit table
class StockLog(Base):
    __tablename__ = "stock_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    change = Column(Integer)
    source = Column(String)
    reference = Column(String)
    note = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# Product table
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    qty = Column(Integer, index=True)

# optional (advanced)
Index("idx_name_qty", ProductDB.name, ProductDB.qty)

# API schema
class Product(BaseModel):
    id: int
    name: str
    qty: int

    class Config:
        from_attributes = True


# User table
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


# User schema
class User(BaseModel):
    username: str
    password: str

# Sale queue
class SaleQueue(Base):
    __tablename__ = "sale_queue"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    qty = Column(Integer)
    status = Column(String, default="pending") # pending, done
    created_at = Column(DateTime, default=datetime.utcnow)

# Product summary
class ProductSummary(Base):
    __tablename__ = "product_summary"

    id = Column(Integer, primary_key=True, index=True)
    total_products = Column(Integer)
    total_qty = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)