import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from routes import auth, payments, orders, health

app = FastAPI(title="Payment Gateway API")

# Registrar rotas
app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(orders.router)
app.include_router(health.router)
