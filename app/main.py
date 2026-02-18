from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import router

app = FastAPI(
    title="User Management System",
    description="A secure user CRUD application with web UI",
    version="1.0.0"
)

# CORS Configuration for production
# Update origins list with your actual frontend domain when deployed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
# Make sure static folder exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API and UI routes
app.include_router(router)

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "User Management API",
        "version": "1.0.0"
    }

# Root endpoint fallback
@app.get("/api")
def api_root():
    """API information endpoint"""
    return {
        "message": "User Management API",
        "docs": "/docs",
        "health": "/health"
    }
