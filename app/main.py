from fastapi import FastAPI
from app import operations
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

app = FastAPI(title="Calculator API")

@app.get("/add")
def add(a: float, b: float):
    return {"result": operations.add(a, b)}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": operations.subtract(a, b)}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": operations.multiply(a, b)}

@app.get("/divide")
def divide(a: float, b: float):
    try:
        return {"result": operations.divide(a, b)}
    except ZeroDivisionError:
        return {"error": "Division by zero not allowed."}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

@app.middleware("http")
async def log_requests(request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

 