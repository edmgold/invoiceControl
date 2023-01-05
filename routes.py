from fastapi import APIRouter

from controllers import debts_controller as debts


router = APIRouter()

router.include_router(debts.router, prefix='/debts', tags=['Debts'])
