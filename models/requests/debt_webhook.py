from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DebtWebhook(BaseModel):
    debtId: int
    paidAt: datetime
    paidAmount: int
    paidBy: str
