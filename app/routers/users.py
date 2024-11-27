from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from ..schemas.user import UserResponse, UserUpdate
from ..services.auth import auth_service
from ..database.mongodb import mongodb
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    db = await mongodb.get_db()
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = await mongodb.get_db()
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = auth_service.get_password_hash(update_data.pop("password"))
    
    if update_data:
        await db.users.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
    
    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    return UserResponse(**updated_user)

@router.post("/me/favorites/teams/{team_id}")
async def add_favorite_team(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = await mongodb.get_db()
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$addToSet": {"favorite_teams": team_id}}
    )
    return {"message": "Team added to favorites"}

@router.delete("/me/favorites/teams/{team_id}")
async def remove_favorite_team(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = await mongodb.get_db()
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"favorite_teams": team_id}}
    )
    return {"message": "Team removed from favorites"} 