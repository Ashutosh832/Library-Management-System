from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class IssueStatus(str, Enum):
    issued = "issued"
    returned = "returned"

class IssueRecordCreate(BaseModel):
    book_id : str
    user_id : str
    issued_date : datetime

class IssueRecordResponse(BaseModel):
    book_id : int
    book_name : str
    user_id : str
    user_name : str
    issued_date : datetime
    return_date : Optional[datetime] = None
    status : IssueStatus

class IssueCreate(BaseModel):
    book_id : str