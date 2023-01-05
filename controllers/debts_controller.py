import ormar

from datetime import datetime, date, timedelta
from fastapi import APIRouter, File, UploadFile, HTTPException

from models.debt import Debts
from models.requests.debt_update import DebtUpdate
from models.requests.debt_webhook import DebtWebhook
from controllers.utils.delete_controller import delete_controller
from controllers.utils.get_all_controller import get_all_controller
from controllers.utils.get_controller import get_controller
from controllers.utils.patch_controller import patch_controller
from controllers.utils.post_controller import post_controller
from controllers.utils.csv_to_json import csv_to_json
from controllers.utils.entity_not_found import entity_not_found

router = APIRouter()


@router.get("/")
@get_all_controller(Debts)
async def list_item():
    pass # pragma: no cover

@router.get("/{id}")
@get_controller(Debts)
async def get_debts(id: int):    
    pass # pragma: no cover

@router.get("/due/{days}")
@entity_not_found
async def get_debts_due(days: int):
    dueDate = date.today() - timedelta(days=days)
    todayDate = date.today()

    return await Debts.objects.all(Debts.debtDueDate<=dueDate, Debts.paidAt==None, ormar.or_(Debts.lastInvoiceSent <= todayDate, Debts.lastInvoiceSent==None) )

@router.post("/")
@post_controller
async def add_item(entity: Debts):
    pass # pragma: no cover

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    result = csv_to_json(file)
    
    if await upload_validate(result):
        for x in result["detail"]:
            x["debtDueDate"] = datetime.strptime(x["debtDueDate"], "%Y-%m-%d")
            debt = Debts(**x) 

            try:
                await debt.save()
            except Exception as ex:
                raise HTTPException(status_code=404, detail=str(ex))

    return result

async def upload_validate(json):
    excepts = {"message": []}

    for x in json["detail"]:
        data = x.copy()
        try:
            # data["debtAmount"] /= 100
            data["debtDueDate"] = datetime.strptime(x["debtDueDate"], "%Y-%m-%d")
        except Exception:
            pass
        
        try:
            debt = Debts(**data)
            try:
                debtId = data["debtId"]
                res = await Debts.objects.get(debtId=debtId)
                excepts["message"].append({"row": x, "error": f"debtId {debtId} ja existe"}) 
            except ormar.exceptions.NoMatch:
                pass
        except ValueError as ex:
            excepts["message"].append({"row": x, "error": str(ex)}) 

    if excepts["message"]:
        raise HTTPException(status_code=404, detail=str(excepts))

    return True    

@router.post("/webhook")
async def webhook(request: DebtWebhook):
    patch = {"debtId": request.debtId, "paidAt": request.paidAt, "paidBy": request.paidBy, "paidAmount": request.paidAmount}

    try:
        res = await Debts.objects.get(debtId=request.debtId)
        await res.update(**patch)
    except:
        return "Parametros inválidos"

    return 'OK'

@router.patch("/{id}")
@patch_controller(Debts)
async def patch_Debts(properties_for_update: DebtUpdate, id: int):
    pass # pragma: no cover

@router.delete("/{id}")
@delete_controller(Debts)
async def delete_Debts(id: int):
    pass # pragma: no cover

