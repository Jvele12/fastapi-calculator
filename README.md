# 🧮 FastAPI Calculator + Secure User Profile

A FastAPI-based web application that provides arithmetic operations along with a **secure user system** supporting registration, login, profile updates, and password changes.

The project demonstrates **modern backend engineering practices**, including:
- SQLAlchemy ORM
- JWT authentication
- Password hashing (bcrypt)
- Dockerized deployment
- Automated testing (unit, integration, E2E)
- CI/CD with GitHub Actions

---

## 🚀 Features

- FastAPI REST API
- User registration & login with JWT authentication
- **User profile update (username/email)**
- **Secure password change with hashing**
- Arithmetic operations (add, subtract, multiply, divide)
- PostgreSQL database integration
- Unit, Integration, and Playwright E2E tests
- Fully Dockerized
- GitHub Actions CI pipeline

---

## 🛠️ Installation & Setup (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/Jvele12/fastapi-calculator.git
cd fastapi-calculator
2. Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the Application
bash
Copy code
uvicorn app.main:app --reload
Visit:

API docs → http://127.0.0.1:8000/docs

🖥️ Using the Web UI
Once running (via Docker or locally):

Register:
http://localhost:8000/register

Login:
http://localhost:8000/login

Profile & Password Management:
http://localhost:8000/profile-ui

From the profile page, users can:

Update username and/or email

Change their password securely

Re-login using the new password

🐳 Running with Docker (Recommended)
bash
Copy code
docker-compose up --build
The app and database will start together in containers.

🧪 Running Tests
bash
Copy code
# Start containers
docker-compose up -d --build

# Run all tests
docker-compose run web pytest -v
Includes:

Unit tests

Integration tests

End-to-end tests using Playwright

📦 Data Models Overview
User Model
Table: users

Fields:

id (PK)

username (unique)

email (unique)

password_hash (bcrypt)

created_at

Schemas:

UserCreate

UserRead

UserUpdate

ProfileUpdate

PasswordChange

Calculation Model
Table: calculations

Fields:

id (PK)

a, b (float)

type (enum: add, sub, multiply, divide)

result

created_at

user_id (optional FK)

Validation:

Division by zero is rejected at schema level.

🔁 CI/CD (GitHub Actions)
Every push to main triggers:

Docker build

PostgreSQL + FastAPI startup

Unit, integration, and Playwright E2E tests

Docker image build & push (on success)

Workflow:

bash
Copy code
.github/workflows/ci.yml
🐳 Docker Hub
Docker image available at:
👉 https://hub.docker.com/r/Jvele12/fastapi-calculator

👨‍💻 Author
Jvele12