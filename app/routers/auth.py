from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..schemas.user import UserCreate, UserResponse, Token
from ..services.auth import auth_service
from ..database.mongodb import mongodb
from ..config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    db = await mongodb.get_db()
    
    # Check if email already exists
    if await db.users.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if await db.users.find_one({"username": user_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash password
    hashed_password = auth_service.get_password_hash(user_data.password)
    
    # Create user document
    user_dict = user_data.dict()
    user_dict["password_hash"] = hashed_password
    del user_dict["password"]  # Remove plain password
    user_dict["favorite_teams"] = []  # Initialize empty favorites list
    
    # Insert into database
    result = await db.users.insert_one(user_dict)
    
    # Get created user and convert _id to string
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])  # Convert ObjectId to string
    return UserResponse(**created_user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = await mongodb.get_db()
    user = await db.users.find_one({"email": form_data.username})  # Using email as username
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_service.verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    # Convert ObjectId to string before passing to Pydantic model
    user["_id"] = str(user["_id"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }

@router.post("/forgot-password")
async def forgot_password(email: str):
    # In a real application, you would:
    # 1. Generate a password reset token
    # 2. Send an email with the reset link
    # 3. Store the token in the database with an expiration
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Password reset functionality not implemented"
    ) 