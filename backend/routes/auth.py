from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user import UserResponse
from sqlalchemy import select
from backend.models.user import User
from backend.core.auth import hash_password, verify_password, create_access_token
from backend.core.dependencies import get_db
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        # 2. Return a 400 instead of letting the DB throw a 500
        raise HTTPException(
            status_code=400, 
            detail="A user with this email already exists."
        )

    # 3. If not exists, proceed with creation
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_admin=False
    )

    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error during registration")

    return new_user
    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Async query for user
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}