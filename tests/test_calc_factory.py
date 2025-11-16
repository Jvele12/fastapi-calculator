import pytest
from app.models import CalculationType
from app.factory import compute

def test_factory_add():
    assert compute(3, 2, CalculationType.add) == 5

def test_factory_sub():
    assert compute(3, 2, CalculationType.sub) == 1

def test_factory_multiply():
    assert compute(3, 2, CalculationType.multiply) == 6

def test_factory_divide():
    assert compute(6, 3, CalculationType.divide) == 2

def test_factory_invalid():
    with pytest.raises(ValueError):
        compute(1, 1, "weird")  # type: ignore
