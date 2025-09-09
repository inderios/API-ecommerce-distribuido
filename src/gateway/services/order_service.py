from sqlalchemy.orm import Session
from gateway.models.order_model import Order
from gateway.common.logger import logger
from gateway.services.cache_service import cache_service


class OrderService:
    """
    Serviço de gerenciamento de pedidos.
    """

    def create_order(self, db: Session, user_id: int, total: float) -> Order:
        """
        Cria um novo pedido.
        """
        try:
            order = Order(user_id=user_id, total=total, status="created")
            db.add(order)
            db.commit()
            db.refresh(order)

            # Salvar no cache
            cache_service.set(f"order:{order.id}:status", order.status)

            logger.info(f"Pedido criado (ID={order.id}, User={user_id}, Total={total})")
            return order
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar pedido: {e}")
            raise e

    def update_order_status(self, db: Session, order_id: int, status: str) -> Order:
        """
        Atualiza o status de um pedido.
        """
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.warning(f"Pedido ID={order_id} não encontrado.")
                return None

            order.status = status
            db.commit()
            db.refresh(order)

            # Atualizar cache
            cache_service.set(f"order:{order.id}:status", order.status)

            logger.info(f"Status atualizado: Order ID={order.id} → {status}")
            return order
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar pedido: {e}")
            raise e

    def get_order_status(self, order_id: int):
        """
        Obtém o status de um pedido (tenta primeiro no cache).
        """
        try:
            cached_status = cache_service.get(f"order:{order_id}:status")
            if cached_status:
                logger.info(f"Status do pedido (cache): ID={order_id} → {cached_status}")
                return cached_status

            logger.info(f"Cache não encontrado para pedido ID={order_id}")
            return None
        except Exception as e:
            logger.error(f"Erro ao consultar pedido no cache: {e}")
            return None


# Instância global
order_service = OrderService()
