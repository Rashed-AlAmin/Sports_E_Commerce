from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.core.auth import decode_access_token
from backend.db.session import SessionLocal
from backend.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_db():

    async with SessionLocal() as session:

        yield session



async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)  # Use AsyncSession
):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    
    # Use select() instead of query()
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def get_current_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user
