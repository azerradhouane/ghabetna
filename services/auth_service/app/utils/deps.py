from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.utils.jwt import decode_token
from sqlalchemy import select

security=HTTPBearer()

async def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    db:AsyncSession=Depends(get_db)
)->User:
    token=credentials.credentials
    try:
        payload=decode_token(token)
        if payload.get("type")!="access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token type")
        user_id=int(payload["sub"])
    except(JWTError,KeyError,ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired Token")
    
    result=await db.execute(select(User).where(User.id==user_id))
    user=result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found or Inactive")
    return user

def require_permission(permission:str):
    """Dependency factory checks permission from JWT payload (decoded in gateway and forwarded as header)"""
    async def checker(
        credentials:HTTPAuthorizationCredentials=Depends(security)
    ):
        try:
            payload=decode_token(credentials.credentials)
            perms=payload.get("permissions",[])
            if permission not in perms:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Insufficient permissions")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    return checker
