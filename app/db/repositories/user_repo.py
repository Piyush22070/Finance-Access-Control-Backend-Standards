from sqlalchemy.orm import Session
from app.db.models.user_model import User


class UserRepository:
    def __init__(self,db:Session):
        self.db=db

    def get_user_by_email(self, email: str):
        users = self.db.query(User).filter(User.email == email).first()
        return users

    def create_user(self,user : User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
  