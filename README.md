# 🧮 FastAPI Calculator + Secure User Model

A simple calculator web API built with **FastAPI** that supports addition, subtraction, multiplication, and division.  
This project includes **unit tests**, **integration tests**, **end-to-end (E2E)** tests with **Playwright**, and a **GitHub Actions CI pipeline**.
This FastAPI application includes arithmetic operations and a secure SQLAlchemy-based User model with hashed passwords. 
It integrates with PostgreSQL, uses Pydantic schemas for validation, and includes CI/CD automation using GitHub Actions and Docker Hub.

---

## 🚀 Features

- REST API built using **FastAPI**
- Endpoints for basic arithmetic operations
- Unit, Integration, and E2E tests
- Logging for requests and responses
- GitHub Actions Continuous Integration (CI)

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Jvele12/fastapi-calculator.git
cd fastapi-calculator
2. Create a Virtual Environment


python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt
4. Run the Application

uvicorn app.main:app --reload
Visit 👉 http://127.0.0.1:8000/docs to test the API.

# FastAPI Secure User Model with CI/CD

## Run locally
```bash
docker-compose up --build

🧩 2. How to Run Tests Locally
### Run Tests Locally
```bash
# Build and start containers
docker-compose up -d --build

# Run tests inside Docker
docker-compose run web pytest -v

### 🐳 3. Docker Hub Link
```markdown
### Docker Hub Repository
Docker image is available here:
👉 [https://hub.docker.com/r/Jvele12/fastapi-calculator](https://hub.docker.com/r/Jvele12/fastapi-calculator)


📦 Data Models Overview
User Model

Table: users

Fields:

id (PK)

username (unique)

email (unique)

password_hash (hashed via passlib[bcrypt])

created_at (timestamp)

Schemas:

UserCreate: username, email, password

UserRead: id, username, email, created_at (no password exposed)

Calculation Model

Table: calculations

Fields:

id (PK)

a (float)

b (float)

type (enum: add, sub, multiply, divide)

result (float, optional)

created_at (timestamp)

user_id (FK to users.id, optional)

Schemas:

CalculationCreate: a, b, type

Validation: for type == "divide", b must not be zero

CalculationRead: id, a, b, type, result, user_id, created_at

A simple factory chooses which operation to perform based on CalculationType.


🔁 CI/CD (GitHub Actions)

Every commit to main triggers:

Build Docker environment

Start Postgres + FastAPI

Run unit tests

Run Playwright E2E tests

If all pass → Build & Push image to Docker Hub

Workflow file: .github/workflows/ci.yml

👨‍💻 Author
Jvele12
