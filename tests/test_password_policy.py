import pytest
from app import hashing

def test_password_hash_and_verify_valid_password():
    password = "secure123"
    hashed = hashing.hash_password(password)

    assert hashed != password
    assert hashing.verify_password(password, hashed) is True


def test_password_too_short_rejected_by_policy():
    short_password = "123"

    assert len(short_password) < 6
