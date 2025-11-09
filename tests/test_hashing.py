from app.hashing import hash_password, verify_password

def test_hash_and_verify():
    pw = "secret"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)
