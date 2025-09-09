# Dockerfile para desenvolvimento da API Gateway
FROM python:3.13-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ./src /app/src

# Expõe a porta da API
EXPOSE 8000

# Rodar Uvicorn com auto-reload
CMD ["uvicorn", "src.gateway.main", "--host", "0.0.0.0", "--port", "8000", "--reload"]
