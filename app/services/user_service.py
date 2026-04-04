from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.database import redis_client
from app.db.models.user_model import User
from app.core.security import security
from app.db.repositories.user_repo import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db=self.db)

    def register_user(self, user_data):
        
        existing_user = self.user_repository.get_user_by_email(email=user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = security.get_password_hash(user_data.password)

        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        user = self.user_repository.create_user(new_user)
        redis_client.sadd(f"users:{user.role}:roles", user.role)
        return user
