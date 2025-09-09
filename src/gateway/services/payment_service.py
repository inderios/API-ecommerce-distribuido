from sqlalchemy.orm import Session
from gateway.models.transaction_model import Transaction
from gateway.common.logger import logger
from gateway.services.cache_service import cache_service


class PaymentService:
    """
    Serviço de gerenciamento de transações financeiras.
    """

    def create_transaction(self, db: Session, user_id: int, order_id: int, amount: float) -> Transaction:
        """
        Cria uma nova transação de pagamento.
        """
        try:
            transaction = Transaction(user_id=user_id, order_id=order_id, amount=amount, status="pending")
            db.add(transaction)
            db.commit()
            db.refresh(transaction)

            # Salvar no cache
            cache_service.set(f"transaction:{transaction.id}:status", transaction.status)

            logger.info(f"Transação criada (ID={transaction.id}, Order={order_id}, Amount={amount})")
            return transaction
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar transação: {e}")
            raise e

    def update_transaction_status(self, db: Session, transaction_id: int, status: str) -> Transaction:
        """
        Atualiza o status de uma transação existente.
        """
        try:
            transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if not transaction:
                logger.warning(f"Transação ID={transaction_id} não encontrada.")
                return None

            transaction.status = status
            db.commit()
            db.refresh(transaction)

            # Atualizar cache
            cache_service.set(f"transaction:{transaction.id}:status", transaction.status)

            logger.info(f"Status atualizado: Transaction ID={transaction.id} → {status}")
            return transaction
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar transação: {e}")
            raise e

    def get_transaction_status(self, transaction_id: int):
        """
        Obtém o status de uma transação (tenta primeiro no cache).
        """
        try:
            # Primeiro tenta no cache
            cached_status = cache_service.get(f"transaction:{transaction_id}:status")
            if cached_status:
                logger.info(f"Status da transação (cache): ID={transaction_id} → {cached_status}")
                return cached_status

            logger.info(f"Cache não encontrado para transação ID={transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Erro ao consultar transação no cache: {e}")
            return None


# Instância global
payment_service = PaymentService()
