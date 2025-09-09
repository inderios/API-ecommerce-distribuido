from sqlalchemy import Column, Integer, String
from gateway.common.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Integer, default=1)  # 1 para ativo, 0 para inativo