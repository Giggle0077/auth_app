from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import List
from .database import SessionLocal, UserDB
from .password_utils import hash_password, verify_password

router = APIRouter()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# ============================================================================
# PYDANTIC MODELS - Enhanced with validation
# ============================================================================

class UserSchema(BaseModel):
    email: EmailStr  # Better email validation
    password: str = Field(..., min_length=8, max_length=72)  # bcrypt limit
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123"
            }
        }

class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility

class PasswordUpdate(BaseModel):
    new_password: str = Field(..., min_length=8, max_length=72)

class MessageResponse(BaseModel):
    message: str

# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_db():
    """Database session dependency with proper cleanup"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# WEB UI ROUTES (Jinja2 Templates)
# ============================================================================

@router.get("/", response_class=HTMLResponse, tags=["Web UI"])
async def home(request: Request, db: Session = Depends(get_db)):
    """Main page displaying all users"""
    users = db.query(UserDB).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "users": users}
    )

@router.get("/register-page", response_class=HTMLResponse, tags=["Web UI"])
async def register_page(request: Request):
    """User registration page"""
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

# ============================================================================
# API ROUTES (JSON endpoints)
# ============================================================================

@router.post("/api/user", status_code=201, response_model=MessageResponse, tags=["API"])
def register(user: UserSchema, db: Session = Depends(get_db)):
    """
    Register a new user with hashed password
    
    SECURITY FIX: Passwords are now hashed instead of stored in plaintext
    BUG FIX: Added proper error handling and response models
    COMPATIBILITY FIX: Uses bcrypt directly instead of passlib
    """
    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before storing
    hashed_pw = hash_password(user.password)
    
    # Create new user
    new_user = UserDB(email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Get the created user with ID
    
    return {"message": "User registered successfully"}

@router.get("/api/users", response_model=List[UserResponse], tags=["API"])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users (passwords excluded from response)
    
    SECURITY FIX: Using response_model to exclude password field
    """
    users = db.query(UserDB).all()
    return users

@router.put("/api/user/change-password/{email}", response_model=MessageResponse, tags=["API"])
def update_password(email: str, data: PasswordUpdate, db: Session = Depends(get_db)):
    """
    Update user password with proper hashing
    
    SECURITY FIX: New password is now hashed
    BEST PRACTICE: More descriptive function name
    """
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Hash the new password
    user.password = hash_password(data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.delete("/api/user/{email}", response_model=MessageResponse, tags=["API"])
def delete_user(email: str, db: Session = Depends(get_db)):
    """
    Delete a user by email
    
    BUG FIX: Added response model for consistency
    """
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

# ============================================================================
# OPTIONAL: Login endpoint (for future implementation)
# ============================================================================

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/api/login", response_model=MessageResponse, tags=["API"])
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    """
    Login endpoint - verifies email and password
    
    Note: In production, you'd want to return a JWT token here
    """
    user = db.query(UserDB).filter(UserDB.email == credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"message": "Login successful"}
