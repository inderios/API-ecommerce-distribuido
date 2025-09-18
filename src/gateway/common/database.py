from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
import os
from dotenv import load_dotenv

from .logger import logger

# Carregar variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/payments_db")

# Redis: sempre usar o host 'redis' para containers Docker
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Base do SQLAlchemy para os modelos
Base = declarative_base()

# Criar Engine do SQLAlchemy
try:
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    logger.info("Conexão com o banco de dados configurada com sucesso.")
except Exception as e:
    logger.error(f"Erro ao configurar conexão com o banco de dados: {e}")
    raise e

# Criar SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar cliente Redis
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()  # Testa conexão
    logger.info("Conexão com Redis configurada com sucesso.")
except Exception as e:
    logger.error(f"Erro ao conectar com Redis: {e}")
    redis_client = None

# Dependência do FastAPI (injeção de sessão por request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
