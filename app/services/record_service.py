import json
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.database import redis_client
from app.db.models.records_model import Record
from app.db.repositories.records_repo import RecordsRepository

class RecordService:
    def __init__(self, db: Session):
        self.db = db
        self.records_repository = RecordsRepository(db=self.db)


    def _invalidate_records_cache(self, record_id: int = None):
        if record_id:
            redis_client.delete(f"records:{record_id}")
        
        cursor = '0'
        while cursor != 0:
            cursor, keys = redis_client.scan(cursor=cursor, match="records:all:*", count=100)
            if keys:
                redis_client.delete(*keys)



    def add_new_record(self,record_data,current_user,request_id):
        if not redis_client.set(f"idempotency:{request_id}", "1" ,nx=True,ex=60):
            raise HTTPException(status_code=400, detail="Request already processed")
        
        if(record_data.amount <= 0):
            raise HTTPException(status_code=400, detail="Amount must be greater than zero")
        

        new_record = Record(
            **record_data.dict(),
            user_id=current_user.id
        )

        saved_record = self.records_repository.create_record(new_record)

        redis_client.delete(f"dashboard:summary:{current_user.id}")
        redis_client.incr("analytics:total_transactions")
        self._invalidate_records_cache()

        return saved_record
    

    
    def get_records(self,skip: int = 0, limit: int = 10):
        cache_key = f"records:all:skip:{skip}:limit:{limit}"
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        records = self.records_repository.get_records(skip=skip, limit=limit)
        
        if records:
            redis_client.setex(cache_key, 300, json.dumps(jsonable_encoder(records)))
        
        return records
    


    def get_record_by_id(self, record_id: int, current_user):
        cache_key = f"records:{record_id}"
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        record = self.records_repository.get_record_by_id(record_id=record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        redis_client.setex(cache_key, 300, json.dumps(jsonable_encoder(record)))
        return record
    


    def update_record(self, record_id: int, update_data: dict, current_user):
        
        record = self.records_repository.get_record_by_id(record_id=record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        updated_record = self.records_repository.update_record(record_id=record_id, update_data=update_data)

        redis_client.delete(f"dashboard:summary:{current_user.id}")
        self._invalidate_records_cache(record_id=record_id)

        return updated_record
    


    def delete_record(self,record_id: int,current_user):
        record = self.records_repository.get_record_by_id(record_id=record_id)

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        success = self.records_repository.delete_record(record_id=record_id)

        if success:
            redis_client.delete(f"dashboard:summary:{current_user.id}")
            self._invalidate_records_cache(record_id=record_id)

        return success

