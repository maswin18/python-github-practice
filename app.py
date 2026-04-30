from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ProductDB, Product, UserDB, User, StockLog
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

# Config
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔧 DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Auth
def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.replace("Bearer ", "")

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# ------------------------
# BASIC
# ------------------------
@app.get("/")
def home():
    return {"message": "API running"}

# ------------------------
# USER
# ------------------------
@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"message": "Invalid credentials"}

    token = jwt.encode(
        {"sub": db_user.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}

# ------------------------
# PRODUCTS
# ------------------------
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {
        "id": db_product.id,
        "name": db_product.name,
        "qty": db_product.qty
    }

@app.get("/products")
def get_products(db: Session = Depends(get_db), user=Depends(verify_token)):
    return db.query(ProductDB).all()

# ------------------------
# SELL (EVENT-BASED)
# ------------------------
@app.post("/sell")
def sell_item(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    product_id = data["id"]
    qty = data["qty"]

    result = db.query(ProductDB).filter(
        ProductDB.id == product_id,
        ProductDB.qty >= qty
    ).update({
        ProductDB.qty: ProductDB.qty - qty
    })

    if result == 0:
        return {"message": "Not enough stock"}

    log = StockLog(
        product_id=product_id,
        change=-qty,
        source="sale",
        reference="order_001",
        note="customer purchase"
    )

    db.add(log)
    db.commit()

    return {"message": "Sale successful"}

# ------------------------
# LOGS
# ------------------------
@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(StockLog).order_by(StockLog.created_at.desc()).all()
