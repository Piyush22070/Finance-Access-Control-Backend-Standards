from sqlalchemy import Column,Integer, String,Float,ForeignKey,Date
from app.db.database import Base

class Record(Base):
    __tablename__ ="records"
    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Float)
    transaction_type = Column(String)
    date = Column(Date, nullable=False)
    category = Column(String)
    note = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    