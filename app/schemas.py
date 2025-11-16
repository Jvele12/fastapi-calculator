from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from typing import Literal, Optional
from datetime import datetime
from .models import CalculationType

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

CalculationTypeLiteral = Literal["add", "sub", "multiply", "divide"]

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType 

    @model_validator(mode="after")
    def check_divide_by_zero(self):
        if self.type == CalculationType.divide and self.b == 0:
            raise ValueError("b cannot be zero for divide")
        return self

class CalculationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    a: float
    b: float
    type: str
    result: Optional[float] = None
    created_at: datetime
    user_id: Optional[int] = None