from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import operations, models, schemas, crud
from .database import Base, engine, SessionLocal
import logging

# Initialize FastAPI
app = FastAPI(title="Calculator & User API")

# === Initialize database ===
Base.metadata.create_all(bind=engine)

# === Logging setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response


# === Calculator Endpoints ===
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


# === Database Dependency ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === User Management Endpoint ===
@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)
