import pytest
from pydantic import ValidationError
from app.schemas import CalculationCreate

def test_divide_by_zero_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=0, type="divide")

def test_invalid_type_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=2, type="pow")  # invalid

def test_valid_create_ok():
    c = CalculationCreate(a=1.5, b=2.5, type="add")
    assert c.a == 1.5 and c.b == 2.5 and c.type == "add"
