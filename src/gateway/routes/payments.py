from fastapi import APIRouter
from gateway.services.cache_service import cache_service

router = APIRouter()

@router.get("/payment-status/{transaction_id}")
def payment_status(transaction_id: str):
    status = cache_service.get(f"transaction:{transaction_id}:status")
    if not status:
        return {"transaction_id": transaction_id, "status": "not found"}
    return {"transaction_id": transaction_id, "status": status}
