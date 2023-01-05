import ormar
import re
import datetime
from pydantic import validator
from db import BaseMeta

class Debts(ormar.Model):
    class Meta(BaseMeta):
        tablename = "debts"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    name: str = ormar.String(max_length=100)
    governmentId: str = ormar.String(max_length=14)
    email: str  = ormar.String(max_length=255)
    debtAmount: float = ormar.Float(minimum=0)
    debtDueDate: datetime = ormar.DateTime(timezone=False)
    debtId: int = ormar.Integer(unique=True)
    paidAt: datetime = ormar.DateTime(timezone=False, default=None, nullable=True)
    paidAmount: float = ormar.Float(minimum=0, default=None ,nullable=True)
    paidBy: str = ormar.String(max_length=100, default=None, nullable=True)
    lastInvoiceSent: datetime = ormar.DateTime(timezone=False, default=None, nullable=True)

    @validator('governmentId')
    def simplified_government_id_validator(cls, v):
        # Check if gid has 11 digits
        if len(v) != 11:
            raise ValueError(f'Government Id need to have 11 digits')

        # check if gid has only numeric digits
        if not re.match(r'^\d+$', v):
            raise ValueError(f'Government Id need to be numeric')

        return v

    @validator('email')
    def email_validator(cls, v):
        if not re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+').match(v):
            raise ValueError(f'Email format is invalid')
        return v     