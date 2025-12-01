from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Enum as SAEnum,
    ForeignKey,
    DateTime,
    func,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CalculationType(str, Enum):
    add = "add"
    sub = "sub"
    multiply = "multiply"
    divide = "divide"


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(
        SAEnum(CalculationType, name="calculation_type"),
        nullable=False,
        index=True,
    )
    result = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    user = relationship("User", backref="calculations")
