from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt

from app.core.config import settings

class Security:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

    def verify_password(self, plain_password,hashed_password):
        return self.pwd_context.verify(plain_password,hashed_password)

    def get_password_hash(self,password):
        return self.pwd_context.hash(password[:71])

    def create_access_token(self,data:dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
        return encoded_jwt

security = Security()