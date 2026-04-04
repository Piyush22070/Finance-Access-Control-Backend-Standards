from typing import List
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt,ExpiredSignatureError
from app.db.database import get_db, redis_client
from app.core.config import settings
from app.db.repositories.user_repo import UserRepository
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token : str= Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY , algorithms=[settings.ALGORITHM])
        email : str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please login again.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    valid_token = redis_client.get(f"session:{user.email}")

    if isinstance(valid_token, bytes):
        valid_token = valid_token.decode('utf-8')

    if not valid_token or valid_token != token:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    return user


def role_required(required_role: List[str]):
    def role_checker(current_user: dict =Depends(get_current_user)):
        is_authorized = False

        # Redis Cache Check
        for roles in required_role:
            if redis_client.sismember(f"user:{current_user.id}:roles", roles):
                is_authorized = True
                break
        
        #If Fails
        if not is_authorized and current_user.role not in required_role:
            raise HTTPException(status_code=403, detail="Access denied.")
    
        return current_user
    
    return role_checker
    


        