from app.db.repositories.user_repo import UserRepository
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schemas import UserCreate, UserResponse
from app.api.dependencies import role_required
from app.services.user_service import UserService

router = APIRouter(
    prefix="/api/users", 
    tags=["users"]
)

#CREATE admin only
@router.post("/", response_model=UserResponse, dependencies=[Depends(role_required("admin"))])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.register_user(user)