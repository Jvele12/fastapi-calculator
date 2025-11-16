from app.database import SessionLocal
from app import schemas, crud, models

def test_insert_calculation_and_fetch():
    db = SessionLocal()
    try:
        payload = schemas.CalculationCreate(a=10, b=4, type="sub")
        calc = crud.create_calculation(db, payload)
        assert calc.id is not None
        assert calc.result == 6
        again = db.query(models.Calculation).get(calc.id)
        assert again is not None
        assert again.type.value == "sub"
    finally:
        db.close()
