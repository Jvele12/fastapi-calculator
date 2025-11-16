from sqlalchemy.orm import Session
from . import models, schemas
from .factory import compute

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


def create_calculation(db: Session, payload: schemas.CalculationCreate, user_id: int | None = None) -> models.Calculation:
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