from fastapi import APIRouter, Depends, HTTPException
from gateway.services.cache_service import cache_service
from sqlalchemy.orm import Session
from gateway.common.database import get_db
from pydantic import BaseModel
from gateway.services.payment_service import payment_service

router = APIRouter()

class CreatePaymentRequest(BaseModel):
    user_id: int
    order_id: int
    amount: float

@router.post("/payments")
def create_payment(request: CreatePaymentRequest, db: Session = Depends(get_db)):
    try:
        transaction = payment_service.create_transaction(db, request.user_id, request.order_id, request.amount)
        return {"transaction_id": transaction.id, "status": transaction.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payment-status/{transaction_id}")
def payment_status(transaction_id: str):
    status = cache_service.get(f"transaction:{transaction_id}:status")
    if not status:
        return {"transaction_id": transaction_id, "status": "not found"}
    return {"transaction_id": transaction_id, "status": status}
