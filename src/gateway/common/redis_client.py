import os
import redis
from dotenv import load_dotenv

from .logger import logger

# Carregar variáveis do .env
load_dotenv()

# URL do Redis (ex: redis://localhost:6379/0)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Criar cliente Redis
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Redis conectado com sucesso.")
except redis.ConnectionError as e:
    logger.error(f"Erro ao conectar no Redis: {e}")
    redis_client = None
