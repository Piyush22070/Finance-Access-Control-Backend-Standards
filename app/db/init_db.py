
from fastapi import HTTPException
from app.core.config import settings
from app.db.database import SessionLocal

from app.db.models.user_model import User
from app.core.security import security


def bootstrap_system():
    try:        
        email = settings.INITIAL_ADMIN_EMAIL
        secret_password = settings.INITIAL_ADMIN_PASSWORD
        db = SessionLocal()
        
        if not db.query(User).filter(User.email == email).first():
            new_user = User(
                email=email,
                role="admin",
                is_active=True,
                hashed_password=security.get_password_hash(secret_password)
            )
            db.add(new_user)
            db.commit()
            
        db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during system bootstrap: {str(e)}")