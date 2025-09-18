from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from gateway.common.database import get_db
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

from pydantic import BaseModel
from gateway.services.order_service import order_service

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

class CreateOrderRequest(BaseModel):
    user_id: int
    total: float

@router.post("/orders")
def create_order(request: CreateOrderRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        order = order_service.create_order(db, request.user_id, request.total)
        return {"order_id": order.id, "status": order.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders")
def get_orders(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.execute("SELECT 1").fetchall()
