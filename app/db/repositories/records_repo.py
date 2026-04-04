from sqlalchemy.orm import Session
from app.db.models.records_model import Record

class RecordsRepository:
    def __init__(self,db: Session):
        self.db =db


    def create_record(self, record_data: Record):
        self.db.add(record_data)
        self.db.commit()
        self.db.refresh(record_data)
        return record_data
    

    def get_records(self, skip: int = 0, limit: int = None):
        query = self.db.query(Record)
        return query.offset(skip).limit(limit).all()


    def get_record_by_id(self, record_id: int):
        records = self.db.query(Record)
        record = records.filter(Record.id == record_id)
        record = record.first()
        return record


    def update_record(self, record_id: int, update_data: dict) -> Record:
        record = self.get_record_by_id(record_id)

        if not record:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        
        for key, value in update_dict.items():
            setattr(record, key, value)
        
        self.db.commit()
        self.db.refresh(record)
        return record


    def delete_record(self, record_id: int) -> bool:
        record = self.get_record_by_id(record_id)

        if not record:
            return False
        
        self.db.delete(record)
        self.db.commit()
        return True