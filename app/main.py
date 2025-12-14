from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import operations, schemas, crud
from app.auth import create_access_token, get_current_user   
from .database import Base, engine, SessionLocal
import logging
import os
import time
from sqlalchemy.exc import OperationalError,  ProgrammingError
from .database import Base, engine, SessionLocal
from fastapi import Body

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


app = FastAPI(title="Calculator & User API")

for attempt in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created (or already exist).")
        break
    except OperationalError:
        print(f"⏳ DB not ready yet (attempt {attempt + 1}/10), sleeping 3s...")
        time.sleep(3)
else:
    raise RuntimeError("❌ Could not connect to the database after multiple attempts.")

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
#  User Endpoints (JWT-based)
# =====================================================

@app.post("/users/", response_model=schemas.UserRead)
def create_user_legacy(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.post("/users/register", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)
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


@app.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

@app.get("/profile", response_model=schemas.UserRead)
def get_profile(current_user=Depends(get_current_user)):
    return current_user


@app.put("/profile", response_model=schemas.UserRead)
def update_profile(
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated = crud.update_user_profile(db, current_user, payload)
    return updated


@app.put("/profile/password")
def update_password(
    payload: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    crud.change_user_password(db, current_user, payload.current_password, payload.new_password)
    return {"message": "Password updated successfully"}


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
    user_id: int | None = None,  
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
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
):
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
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    updated = crud.update_calculation(db, calc_id, payload)
    return updated


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation_endpoint(
    calc_id: int,
    db: Session = Depends(get_db),
):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    crud.delete_calculation(db, calc_id)
    return None

# =====================================================
#  Front-end pages (HTML)
# =====================================================

@app.get("/register")
def register_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "register.html"))


@app.get("/login")
def login_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "login.html"))

@app.get("/profile-ui")
def profile_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "profile.html"))


# =====================================================
#  JWT API endpoints
# =====================================================

@app.post("/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user_jwt(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.error(f"Error ensuring tables exist: {e}")

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = crud.create_user(db, user)
    token = create_access_token({"sub": str(new_user.id)})

    return {"access_token": token, "token_type": "bearer"}



@app.post("/login", response_model=schemas.TokenResponse)
def login_user_jwt(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/calculations-ui")
def calculations_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "calculations.html"))
