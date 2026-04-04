from datetime import date

from fastapi import APIRouter, Depends,Header,Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.record_schemas import RecordCreate, RecordResponse, RecordUpdate
from app.services.record_service import RecordService
from app.api.dependencies import role_required, get_current_user

router = APIRouter(
    prefix="/api/records", 
    tags=["records"]
)

# CREATE admin and analyst with idempotency
@router.post("/", response_model=RecordResponse, dependencies=[Depends(role_required("admin"))])
def create_record(
    record: RecordCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    x_request_id: str = Header(...)
):
    record_service = RecordService(db)
    return record_service.add_new_record(record, current_user,x_request_id)



# READ ALL admin, analyst
@router.get("/", response_model=List[RecordResponse],dependencies=[Depends(role_required(["admin","analyst"]))])
def get_all_records(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100),
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Filter by category (e.g., Food, Rent)"),
    transaction_type: Optional[str] = Query(None, description="Filter by type (e.g., income, expense)"),
    db: Session = Depends(get_db),
):
    record_service = RecordService(db)
    return record_service.get_records(
        skip=skip, 
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category=category,
        transaction_type=transaction_type
    )




# READ ID wise admin, analyst and viewer
@router.get("/{record_id}",response_model=RecordResponse, dependencies=[Depends(role_required(["admin","analyst"]))])
def get_record(
    record_id: int,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    record_service = RecordService(db)
    record = record_service.get_record_by_id(record_id, current_user)
    return record



# UPDATE admin only
@router.patch("/{record_id}", response_model=RecordResponse, dependencies=[Depends(role_required(["admin"]))])
def update_record(
    record_id: int,
    record: RecordUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    record_service = RecordService(db)
    return record_service.update_record(record_id, record, current_user)



#DELETE admin only
@router.delete("/{record_id}", dependencies=[Depends(role_required("admin"))])
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    record_service = RecordService(db)
    return record_service.delete_record(record_id, current_user)



