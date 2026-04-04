from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import auth_service
from app.api.dependencies import oauth2_scheme

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    auth_service.blacklist_token(token) 
    return {"message": "Successfully logged out"}
    