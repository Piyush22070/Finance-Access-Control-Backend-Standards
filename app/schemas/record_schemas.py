from pydantic import BaseModel,Field, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum

class TransactionTypeEnum(str,Enum):
    income ="income"
    expense ="expense"

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount of the transaction")
    transaction_type : TransactionTypeEnum
    category : str
    date : date
    note : Optional[str] = None


class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount : Optional[float] = Field(None, gt=0)
    transaction_type : Optional[TransactionTypeEnum] = None
    category : Optional[str] = None
    date : Optional[date] = None  # type:ignore
    note : Optional[str] = None

class RecordResponse(RecordBase):
    id : int
    user_id : int

    model_config = ConfigDict(from_attributes=True)


