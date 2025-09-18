
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gateway.main import app
from gateway.common.database import SessionLocal
from gateway.models.user_model import User

client = TestClient(app)

def test_e2e_payment_flow():
	# Garantir que o usuário de teste existe
	db = SessionLocal()
	user = db.query(User).filter_by(id=1).first()
	if not user:
		user = User(id=1, username="admin", email="admin@example.com", password_hash="fakehash", full_name="Admin Test", is_active=1)
		db.add(user)
		db.commit()
	db.close()
	# 1. Login e obtenção do token
	login_resp = client.post("/auth/login", json={"username": "admin", "password": "admin"})
	assert login_resp.status_code == 200
	token = login_resp.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}

	# 2. Criar pedido
	order_resp = client.post("/orders", json={"user_id": 1, "total": 100.0}, headers=headers)
	assert order_resp.status_code == 200
	order_id = order_resp.json()["order_id"]

	# 3. Criar pagamento
	payment_resp = client.post("/payments", json={"user_id": 1, "order_id": order_id, "amount": 100.0})
	assert payment_resp.status_code == 200
	transaction_id = payment_resp.json()["transaction_id"]

	# 4. Consultar status do pagamento
	status_resp = client.get(f"/payment-status/{transaction_id}")
	assert status_resp.status_code == 200
	assert status_resp.json()["status"] in ["pending", "not found"]
