from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
from decimal import Decimal

class WishStatus(str, Enum):
    open      = "open"
    taken     = "taken"
    completed = "completed"
    cancelled = "cancelled"

class Category(BaseModel):
    id: int
    name: str

class Wish(BaseModel):
    id: int
    id_requester: int
    id_category: int
    description: str
    amount: Decimal
    currency: str
    deadline: date
    status: WishStatus
    created_at: datetime
