import os
from dotenv import load_dotenv
from fastapi import FastAPI
import redis

# 1️⃣ Carregar variáveis do .env
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

# 2️⃣ Conexão com Redis
try:
    redis_client = redis.Redis.from_url(REDIS_URL)
    redis_client.ping()
    print("Redis conectado com sucesso!")
except redis.ConnectionError:
    print("Falha ao conectar no Redis.")

# 3️⃣ Inicializar FastAPI
app = FastAPI(title="Payment Gateway API")

# 4️⃣ Rotas básicas
@app.get("/")
async def root():
    return {"message": "Payment Gateway API está rodando "}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/redis-test")
async def redis_test():
    try:
        redis_client.set("teste", "funcionando")
        value = redis_client.get("teste").decode("utf-8")
        return {"redis_value": value}
    except Exception as e:
        return {"error": str(e)}
    
# Incluir rotas de outros módulos