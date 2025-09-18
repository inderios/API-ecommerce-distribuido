import os
import redis
from dotenv import load_dotenv

from .logger import logger

# Carregar variáveis do .env
load_dotenv()

# URL do Redis (ex: redis://localhost:6379/0)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

from urllib.parse import urlparse, urlunparse

def get_alternate_url(url):
    # Only swap the hostname, preserve scheme and port
    parsed = urlparse(url)
    hostname = parsed.hostname
    if hostname == "localhost":
        new_hostname = "redis"
    elif hostname == "redis":
        new_hostname = "localhost"
    else:
        return url  # No swap needed
    # Rebuild the URL with the new hostname
    netloc = f"{new_hostname}:{parsed.port}" if parsed.port else new_hostname
    new_url = urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
    return new_url

# Criar cliente Redis com fallback
redis_client = None
for url in [REDIS_URL, get_alternate_url(REDIS_URL)]:
    try:
        redis_client = redis.Redis.from_url(url, decode_responses=True)
        redis_client.ping()
        logger.info(f"Redis conectado com sucesso usando: {url}")
        break
    except redis.ConnectionError as e:
        logger.error(f"Erro ao conectar no Redis ({url}): {e}")
        redis_client = None
