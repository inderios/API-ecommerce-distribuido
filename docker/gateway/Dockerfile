FROM python:3.11-slim
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt .
# Install system dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000 
# Expõe a porta da API