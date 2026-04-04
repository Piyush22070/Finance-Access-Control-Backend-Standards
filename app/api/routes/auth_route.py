from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(db: Session = Depends(get_db)):
    ...
    