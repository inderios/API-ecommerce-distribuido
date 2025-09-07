from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(username: str, password: str):
    return {"message": f"Usuário {username} logado com sucesso"}
