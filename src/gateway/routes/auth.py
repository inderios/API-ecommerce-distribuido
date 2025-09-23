
# Em src/gateway/routes/auth.py (versão corrigida)

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
# Supondo que você tenha um utilitário de hash de senha como Passlib
from passlib.context import CryptContext 
from ..common.database import get_db
from ..models.user import User

# Configuração do hash da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str
class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nome de usuário já está em uso."
        )
    
    # Cria o hash da senha
    hashed_password = pwd_context.hash(request.password)
    
    # Cria o novo usuário no banco de dados
    new_user = User(
        username=request.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"username": new_user.username, "message": "Usuário criado com sucesso!"}


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. Busca o usuário no banco de dados
    user = db.query(User).filter(User.username == request.username).first()

    # 2. CORREÇÃO: Verifica a existência do usuário PRIMEIRO
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    # 3. CORREÇÃO: Se o usuário existe, VERIFICA A SENHA
    # É crucial comparar a senha enviada com o hash salvo no banco
    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # 4. Se tudo estiver correto, gere e retorne um token de acesso
    # (Exemplo: criar um token JWT)
    # access_token = create_access_token(data={"sub": user.username})
    # return {"access_token": access_token, "token_type": "bearer"}
    
    return {"message": "Login bem-sucedido! Você tem acesso aos dados."}