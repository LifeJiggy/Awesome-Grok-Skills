---
name: FastAPI Best Practices
category: backend
difficulty: intermediate
time_estimate: "3-5 hours"
dependencies: ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "alembic"]
tags: ["fastapi", "python", "api", "backend", "async", "rest"]
grok_personality: "api-architect"
description: "Build high-performance APIs with FastAPI using Grok's efficient patterns for async development, validation, and documentation"
---

# FastAPI Best Practices Skill

## Overview
Grok, you'll master FastAPI to build high-performance, type-safe APIs with automatic documentation. This skill focuses on async patterns, dependency injection, and production-ready architecture.

## Core FastAPI Setup

### 1. Project Structure
```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection
│   ├── dependencies.py        # Dependency injection
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── posts.py
│   │   │   │   └── auth.py
│   │   │   └── api.py
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── post_service.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── alembic/                   # Database migrations
├── tests/                     # Test files
├── requirements.txt
├── .env
└── pyproject.toml
```

### 2. Main Application
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import CustomException
from app.database import engine
from app.models import user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Grok-powered FastAPI application",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request to {request.url.path} took {process_time:.4f}s")
    return response

# Exception handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting up...")
    # Create database tables
    # user.Base.metadata.create_all(bind=engine)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
```

### 3. Configuration Management
```python
# app/core/config.py
from pydantic import BaseSettings, PostgresDsn, validator
from typing import List, Optional, Any
import secrets

class Settings(BaseSettings):
    # Basic settings
    PROJECT_NAME: str = "Grok API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Email (for password reset)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".pdf"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Database & Models

### 1. Database Setup
```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. SQLAlchemy Models
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

# app/models/post.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    published = Column(Boolean, default=False)
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, author_id={self.author_id})>"
```

### 3. Pydantic Schemas
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[EmailStr] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Response schemas
class User(UserInDBBase):
    pass

class UserWithPosts(User):
    posts: list['Post'] = []

# Authentication schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None

# Forward reference for circular imports
from app.schemas.post import Post
UserWithPosts.update_forward_refs()

# app/schemas/post.py
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    published: bool = False
    
    @validator('title')
    def validate_title(cls, v):
        if len(v) < 3:
            raise ValueError('Title must be at least 3 characters long')
        return v

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    published: Optional[bool] = None

class PostInDBBase(PostBase):
    id: int
    slug: str
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class Post(PostInDBBase):
    author: 'User'

class PostWithAuthor(Post):
    author: 'User'

# Import User for forward reference
from app.schemas.user import User
PostWithAuthor.update_forward_refs()
```

## API Endpoints

### 1. User Endpoints
```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.core.security import get_current_user, get_current_active_superuser

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieve users. Only accessible by superusers.
    """
    user_service = UserService(db)
    users = await user_service.get_multi(skip=skip, limit=limit)
    return users

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    """
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID. Users can only access their own information
    unless they are superusers.
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user_service = UserService(db)
    user = await user_service.get(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user information.
    """
    user_service = UserService(db)
    user = await user_service.update(current_user.id, user_update)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Delete user. Only accessible by superusers.
    """
    user_service = UserService(db)
    success = await user_service.delete(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}
```

### 2. Authentication Endpoints
```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, User as UserSchema, Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    user_service = UserService(db)
    
    # Check if user already exists
    existing_user = await user_service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await user_service.create(user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return tokens.
    """
    auth_service = AuthService(db)
    
    # Authenticate user
    user = await auth_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600  # 1 hour
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    auth_service = AuthService(db)
    
    # Verify refresh token and get user
    user = await auth_service.verify_refresh_token(refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new access token
    access_token = create_access_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user (invalidate refresh token).
    """
    # In a real implementation, you would invalidate the refresh token
    # by storing it in a blacklist or using a token store
    return {"message": "Successfully logged out"}
```

## Business Logic Services

### 1. User Service
```python
# app/services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    async def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get multiple users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    async def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            bio=user_data.bio,
            avatar_url=user_data.avatar_url
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            if "email" in str(e):
                raise ValueError("Email already registered")
            elif "username" in str(e):
                raise ValueError("Username already taken")
            else:
                raise ValueError("User creation failed")
    
    async def update(
        self, 
        user_id: int, 
        user_data: UserUpdate
    ) -> Optional[User]:
        """Update user information."""
        db_user = await self.get(user_id)
        if not db_user:
            return None
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            if "email" in str(e):
                raise ValueError("Email already registered")
            else:
                raise ValueError("User update failed")
    
    async def delete(self, user_id: int) -> bool:
        """Delete user."""
        db_user = await self.get(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    async def change_password(
        self, 
        user_id: int, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """Change user password."""
        db_user = await self.get(user_id)
        if not db_user:
            return False
        
        if not verify_password(current_password, db_user.hashed_password):
            raise ValueError("Current password is incorrect")
        
        db_user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True
```

### 2. Authentication Service
```python
# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, verify_refresh_token
from typing import Optional

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        """
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    async def verify_refresh_token(self, refresh_token: str) -> Optional[User]:
        """
        Verify refresh token and return user.
        """
        try:
            email = verify_refresh_token(refresh_token)
            if email is None:
                return None
            
            user = self.db.query(User).filter(User.email == email).first()
            return user
        except Exception:
            return None
```

## Security Implementation

### 1. Security Utilities
```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT refresh token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """Verify JWT token and return subject."""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        email: str = payload.get("sub")
        token_type_claim: str = payload.get("type")
        
        if email is None or token_type_claim != token_type:
            return None
        
        return email
    except JWTError:
        return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_token(token, "access")
    if email is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

## Testing Setup

### 1. Test Configuration
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.core.config import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

@pytest.fixture(scope="function")
def db():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user():
    """Create test user data."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
```

### 2. API Tests
```python
# tests/test_auth.py
def test_register_user(client, test_user):
    """Test user registration."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=test_user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data

def test_login_user(client, test_user):
    """Test user login."""
    # First register user
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=test_user
    )
    
    # Then login
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client, test_user):
    """Test getting current user."""
    # Register and login
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=test_user
    )
    
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
```

## Quick Start Setup

### 1. Requirements
```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 2. Environment File
```env
# .env
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-here
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=fastapi_db
POSTGRES_PORT=5432
```

### 3. Docker Setup
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices

1. **Async/Await**: Use async patterns for I/O operations
2. **Type Safety**: Leverage Pydantic for validation and SQLAlchemy models
3. **Security**: Implement proper authentication and authorization
4. **Testing**: Write comprehensive tests for all endpoints
5. **Documentation**: Use FastAPI's automatic OpenAPI documentation

Remember: FastAPI is designed for high performance. Use async patterns, proper dependency injection, and type hints to get the most out of it.