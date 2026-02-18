# FastAPI Auth App (Email + Password)

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000

## Project Structure

```
auth_app/
├── main.py
├── requirements.txt
└── templates/
    ├── base.html
    ├── home.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    └── reset_password.html
```

## Features

| Feature | Details |
|---|---|
| **Register** | Email validation, password strength check (8+ chars, upper, lower, digit, special), duplicate email guard |
| **Login** | Email + password verification using bcrypt |
| **Reset Password** | Lookup by email, enforce new password strength |
| **Password Hashing** | bcrypt via `passlib` |
| **Frontend** | Jinja2 templates with live password-strength indicator |

## Password Rules

- Minimum 8 characters  
- At least one uppercase letter  
- At least one lowercase letter  
- At least one digit  
- At least one special character (`!@#$%^&*` etc.)

> **Note:** This uses an in-memory dict as the user store. Replace `fake_users_db` with a real database (e.g. SQLAlchemy + PostgreSQL) for production use.
