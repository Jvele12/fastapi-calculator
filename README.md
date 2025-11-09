# 🧮 FastAPI Calculator

A simple calculator web API built with **FastAPI** that supports addition, subtraction, multiplication, and division.  
This project includes **unit tests**, **integration tests**, **end-to-end (E2E)** tests with **Playwright**, and a **GitHub Actions CI pipeline**.

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

🧪 Running Tests
Unit & Integration Tests

pytest -v
End-to-End Tests (Playwright)

pytest tests/test_e2e_playwright.py

🧰 Continuous Integration (GitHub Actions)
This project includes a CI workflow (.github/workflows/ci.yml) that automatically:

Installs dependencies

Runs tests on each push

Reports test results in the Actions tab

👨‍💻 Author
Jvele12
