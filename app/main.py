from fastapi import FastAPI
from app import operations
import logging

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


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

@app.middleware("http")
async def log_requests(request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response