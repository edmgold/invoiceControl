from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DebtUpdate(BaseModel):
    paidAt: Optional[datetime] = None
    paidAmount: Optional[int] = None
    paidBy: Optional[str] = None
    lastInvoiceSent: Optional[datetime] = None
