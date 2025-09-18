from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from jose import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginRequest(BaseModel):
    username: str
    password: str

def authenticate_user(username: str, password: str):
    # Exemplo simples, substitua por consulta ao banco de dados
    if username == "admin" and password == "admin":
        return True
    return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(request: LoginRequest):
    if not authenticate_user(request.username, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    access_token = create_access_token({"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}
