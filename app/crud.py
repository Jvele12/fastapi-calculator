from sqlalchemy.orm import Session
from . import models, schemas, hashing

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
