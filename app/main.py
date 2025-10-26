from fastapi import FastAPI
from app import operations

app = FastAPI(title="Calculator API")

@app.get("/add")
def add(a: float, b: float):
    return {"result": operations.add(a, b)}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": operations.subtract(a, b)}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": operations.multiply(a, b)}

@app.get("/divide")
def divide(a: float, b: float):
    try:
        return {"result": operations.divide(a, b)}
    except ZeroDivisionError:
        return {"error": "Division by zero not allowed."}
