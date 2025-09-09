from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gateway.common.database import get_db

router = APIRouter()

@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.execute("SELECT 1").fetchall()
