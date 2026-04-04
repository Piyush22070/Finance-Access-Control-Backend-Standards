from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import redis_client
from app.core.security import security
from app.db.repositories.user_repo import UserRepository

class AuthService:
    def __init__(self):
        self.db = None

    def authenticate_user(self, db: Session, email: str,password: str):

        user_repository = UserRepository(db)

        user = user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        if not security.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token = security.create_access_token({"sub": user.email,"role": user.role})
        
        redis_client.set(f"session:{user.email}",token,ex=1800) 

        return token
    
auth_service = AuthService() 