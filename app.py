from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ProductDB, Product, UserDB, User
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def home():
    return {"message": "API with DB running"}

@app.get("/products")
def get_products(
        db: Session = Depends(get_db),         
        user=Depends(verify_token)
    ):
    return db.query(ProductDB).all()

@app.post("/products")
def add_products(product: Product, db:Session = Depends(get_db)):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated: Product, db:Session = Depends(get_db)):
    p = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not p:
        return {"message": "Product not found"}
    
    p.name = updated.name
    p.qty = updated.qty
    db.commit()
    return p

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not p:
        return {"message": "Product not found"}
    
    db.delete(p)
    db.commit()
    return {"message": "Deleted"}

@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(
        username = user.username,
        password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created", "username": db_user.username}

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"message": "Invalid credentials"}
    
    # Create token
    token_data = {
        "sub": db_user.username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}
