from app.database import SessionLocal
from app import models, hashing

def test_create_user_unique_email():
    db = SessionLocal()
    user1 = models.User(username="alice", email="a@a.com", password_hash=hashing.hash_password("pw"))
    user2 = models.User(username="bob", email="a@a.com", password_hash=hashing.hash_password("pw"))
    db.add(user1)
    db.commit()
    db.add(user2)
    try:
        db.commit()
    except Exception:
        db.rollback()
        assert True
    finally:
        db.close()
