from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

class User(BaseModel):
    id: int               # внутр. PK
    telegram_id: int
    username: str
    karma_level: int
    account_status: str
    created_at: datetime
    preferred_categories: List[int]

class User(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str]
    karma_level: int
    account_status: str
    created_at: datetime
    preferred_categories: List[int] = []

class DealMessage(BaseModel):
    id: int
    id_deal: int
    sender_id: int
    message: str
    sent_at: datetime

class WishQuestion(BaseModel):
    id: int
    id_wish: int
    sender_id: int
    receiver_id: int
    question: str
    answer: str | None = None
    created_at: datetime

class WishStatus(str, Enum):
    open      = "open"
    taken     = "taken"
    completed = "completed"
    cancelled = "cancelled"

class DealStatus(str, Enum):
    active    = "active"
    finished  = "finished"
    failed    = "failed"
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

class Deal(BaseModel):
    id: int
    id_wish: int
    id_wishmaker: int
    start_date: datetime
    end_date: Optional[datetime]
    status: DealStatus
    telegram_chat_id: Optional[int]
    chat_enabled: bool
    new_amount: Optional[Decimal]
    new_currency: Optional[str]
    change_requested_by: Optional[int]
    change_status: Optional[str]