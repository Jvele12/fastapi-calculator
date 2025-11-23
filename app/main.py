from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app import operations, schemas, crud
from .database import Base, engine, SessionLocal
import logging

app = FastAPI(title="Calculator & User API")

Base.metadata.create_all(bind=engine)

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


# =====================================================
#  Core Calculator Endpoints (existing)
# =====================================================

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


# =====================================================
#  DB Dependency
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
#  User Endpoints
# =====================================================

@app.post("/users/", response_model=schemas.UserRead)
def create_user_legacy(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.post("/users/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.post("/users/login", response_model=schemas.UserRead)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return user


# =====================================================
#  Calculation BREAD Endpoints
# =====================================================

@app.post(
    "/calculations",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation_endpoint(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    user_id: int | None = None,  # Optional for now (no auth yet)
):
    calc = crud.create_calculation(db, payload, user_id=user_id)
    return calc


@app.get("/calculations", response_model=list[schemas.CalculationRead])
def browse_calculations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
):
    calcs = crud.list_calculations(db, skip=skip, limit=limit, user_id=user_id)
    return calcs


@app.get("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@app.put("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation_endpoint(
    calc_id: int,
    payload: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calc = crud.update_calculation(db, calc_id, payload)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation_endpoint(calc_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_calculation(db, calc_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return None
