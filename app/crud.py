from sqlalchemy.orm import Session
from . import models, schemas, hashing
from .factory import compute
from fastapi import HTTPException

# ======================
# USER CRUD
# ======================

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hashing.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def verify_user_credentials(db: Session, email: str, password: str) -> models.User | None:
    """
    For POST /users/login:
    - Returns the user if email exists and password is correct.
    - Returns None otherwise.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not hashing.verify_password(password, user.password_hash):
        return None
    return user

def update_user_profile(db: Session, current_user: models.User, payload: schemas.ProfileUpdate) -> models.User:
    user = db.get(models.User, current_user.id)
    if not user:
        raise ValueError("User not found")

    if payload.username is not None:
        user.username = payload.username
    if payload.email is not None:
        user.email = payload.email

    db.commit()
    db.refresh(user)
    return user


def change_user_password(
    db: Session,
    current_user: models.User,
    current_password: str,
    new_password: str,
) -> models.User:
    user = db.get(models.User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not hashing.verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user.password_hash = hashing.hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user




# ======================
# CALCULATION CRUD
# ======================

def create_calculation(
    db: Session,
    payload: schemas.CalculationCreate,
    user_id: int | None = None
) -> models.Calculation:
    op = models.CalculationType(payload.type)
    result = compute(payload.a, payload.b, op)

    calc = models.Calculation(
        a=payload.a,
        b=payload.b,
        type=op,
        result=result,
        user_id=user_id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def get_calculation(db: Session, calc_id: int) -> models.Calculation | None:
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()


def list_calculations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
):
    q = db.query(models.Calculation)
    if user_id is not None:
        q = q.filter(models.Calculation.user_id == user_id)
    return q.offset(skip).limit(limit).all()


def update_calculation(
    db: Session,
    calc_id: int,
    payload: schemas.CalculationUpdate,
) -> models.Calculation | None:
    calc = get_calculation(db, calc_id)
    if not calc:
        return None

    if payload.a is not None:
        calc.a = payload.a
    if payload.b is not None:
        calc.b = payload.b
    if payload.type is not None:
        calc.type = payload.type

    calc.result = compute(calc.a, calc.b, calc.type)

    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc_id: int) -> bool:
    calc = get_calculation(db, calc_id)
    if not calc:
        return False
    db.delete(calc)
    db.commit()
    return True
