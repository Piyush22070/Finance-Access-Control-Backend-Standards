from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    analytics_service = AnalyticsService(db)
    summary_data = analytics_service.get_dashboard_summary(current_user)
    return summary_data
