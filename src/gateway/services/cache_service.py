from gateway.common.redis_client import redis_client
from gateway.common.logger import logger

class CacheService:
    """Serviço para interagir com o Redis (cache)."""

    def __init__(self, client=redis_client):
        self.client = client

    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """
        Armazena um valor no cache com TTL (em segundos).
        """
        if not self.client:
            logger.warning("Redis indisponível. Cache ignorado.")
            return False
        try:
            self.client.set(key, value, ex=expire)
            logger.info(f"Cache definido para chave: {key}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar no cache: {e}")
            return False

    def get(self, key: str):
        """
        Recupera um valor do cache.
        """
        if not self.client:
            logger.warning("Redis indisponível. Cache ignorado.")
            return None
        try:
            value = self.client.get(key)
            logger.info(f"Cache lido para chave: {key}")
            return value
        except Exception as e:
            logger.error(f"Erro ao ler do cache: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Remove uma chave do cache.
        """
        if not self.client:
            logger.warning("Redis indisponível. Cache ignorado.")
            return False
        try:
            self.client.delete(key)
            logger.info(f"Cache removido para chave: {key}")
            return True
        except Exception as e:
            logger.error(f"Erro ao remover do cache: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Verifica se uma chave existe no cache.
        """
        if not self.client:
            return False
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar chave no cache: {e}")
            return False


# Instância global para uso em outros módulos
cache_service = CacheService()
