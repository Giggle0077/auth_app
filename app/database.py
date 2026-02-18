from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

Base = declarative_base()

class UserDB(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Stores bcrypt hash

# Get database URL from environment variable
# Render automatically provides DATABASE_URL for PostgreSQL databases
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/dbname"  # Fallback for local development
)

# Render uses 'postgres://' but SQLAlchemy needs 'postgresql://'
# This handles both formats
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling for production
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,        # Number of permanent connections
    max_overflow=20,     # Additional connections when needed
    echo=False           # Set to True for SQL query logging in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize tables when module is imported
init_db()
